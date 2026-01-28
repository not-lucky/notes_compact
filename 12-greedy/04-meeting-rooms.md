# Meeting Rooms

> **Prerequisites:** [Merge Intervals](./03-merge-intervals.md)

## Interview Context

Meeting rooms tests:

1. **Interval overlap detection**: Can all meetings happen in one room?
2. **Resource allocation**: Minimum rooms needed
3. **Algorithm choice**: Sorting vs heap vs sweep line
4. **Optimization skills**: Multiple valid approaches

---

## Building Intuition

**Meeting Rooms I: The "One Room" Question**

Can all meetings fit in a single room? This is just asking: "Do any meetings overlap?"

Think of it as: if we lay all meetings on a timeline, do any of them stack on top of each other?

```
Meetings: [0,30], [5,10], [15,20]

Timeline:
0----5----10---15---20---25---30
|============================|     [0,30]
     |===|                        [5,10]
               |=====|            [15,20]
     ↑
     Overlap here! Need 2 rooms.
```

**Meeting Rooms II: The "Peak Concurrency" Question**

How many meetings overlap at the worst moment? That's the minimum number of rooms.

Mental model: Imagine a graph of "meetings in progress" over time:

```
Time:     0   5   10  15  20  25  30
Rooms:    1   2    1   2   1   1   0
              ↑         ↑
           Peak at 2 rooms needed
```

**The Three Equivalent Views**

Meeting Rooms II can be solved three ways, all giving the same answer:

1. **Min-Heap (Greedy Room Reuse)**:
   - Track when each room becomes free
   - For new meeting: reuse earliest-freeing room if possible
   - If can't reuse, open new room

2. **Sweep Line (Event Counting)**:
   - +1 at each meeting start
   - -1 at each meeting end
   - Maximum concurrent meetings = answer

3. **Two Pointers (Sorted Events)**:
   - Sort starts and ends separately
   - Walk through, counting active meetings

---

## When NOT to Use These Approaches

**1. When Rooms Have Different Capacities**

If rooms have size limits (room A fits 10 people, room B fits 50):

```
This becomes a bin packing / assignment problem,
typically solved with greedy heuristics or optimization.
```

**2. When Meetings Have Preferences**

If some meetings must be in specific rooms, or some rooms are preferred:

```
This becomes a constrained assignment problem.
May need matching algorithms or constraint satisfaction.
```

**3. When You Need the Actual Schedule**

If you need to output "meeting X → room Y":

```
Heap approach naturally gives this!
Each pop/push represents room assignment.
Sweep line only gives the count, not assignments.
```

**4. When Intervals Can Be Rescheduled**

If you can move meetings to minimize rooms:

```
That's job scheduling with flexibility—much harder!
Our algorithms assume fixed meeting times.
```

---

## Meeting Rooms I: Conflict Detection

### Problem Statement

Given an array of meeting time intervals, determine if a person can attend all meetings.

```
Input:  intervals = [[0,30], [5,10], [15,20]]
Output: false (meetings [0,30] and [5,10] overlap)

Input:  intervals = [[7,10], [2,4]]
Output: true (no overlap)
```

### Solution

```python
def can_attend_meetings(intervals: list[list[int]]) -> bool:
    """
    Check if all meetings can be attended (no overlaps).

    Time: O(n log n) for sorting
    Space: O(1)
    """
    if len(intervals) <= 1:
        return True

    # Sort by start time
    intervals.sort(key=lambda x: x[0])

    for i in range(1, len(intervals)):
        # If current meeting starts before previous ends → conflict
        if intervals[i][0] < intervals[i-1][1]:
            return False

    return True
```

### Visual Example

```
Intervals: [[0,30], [5,10], [15,20]]

After sort: [[0,30], [5,10], [15,20]]

Timeline:
[0,30]: |------------------------------|
[5,10]:     |-----|
[15,20]:              |-----|

Check:
- [5,10] starts at 5 < 30 (end of [0,30]) → CONFLICT!

Return: false
```

---

## Meeting Rooms II: Minimum Rooms

### Problem Statement

Given an array of meeting intervals, find the minimum number of conference rooms required.

```
Input:  intervals = [[0,30], [5,10], [15,20]]
Output: 2

Explanation:
- Room 1: [0,30]
- Room 2: [5,10], then [15,20]
```

---

## Approach 1: Min-Heap (Recommended)

Track the end times of ongoing meetings in a min-heap.

```python
import heapq

def min_meeting_rooms(intervals: list[list[int]]) -> int:
    """
    Find minimum meeting rooms needed using min-heap.

    Key insight: Track earliest ending meeting.
    If new meeting starts after earliest ends, reuse that room.

    Time: O(n log n)
    Space: O(n) for heap
    """
    if not intervals:
        return 0

    # Sort by start time
    intervals.sort(key=lambda x: x[0])

    # Min-heap of end times (rooms in use)
    heap = []
    heapq.heappush(heap, intervals[0][1])

    for start, end in intervals[1:]:
        # If earliest ending meeting has ended, remove it
        if start >= heap[0]:
            heapq.heappop(heap)

        # Add current meeting's end time
        heapq.heappush(heap, end)

    # Heap size = number of rooms in use
    return len(heap)
```

### Visual Trace

```
Intervals: [[0,30], [5,10], [15,20]]
Sorted:    [[0,30], [5,10], [15,20]]

Step 1: [0,30]
  heap = [30]
  rooms = 1

Step 2: [5,10]
  start=5 < heap[0]=30 → can't reuse room
  heap = [10, 30]
  rooms = 2

Step 3: [15,20]
  start=15 >= heap[0]=10 → reuse room (pop 10)
  heap = [20, 30]
  rooms = 2

Answer: 2
```

---

## Approach 2: Sweep Line (Event-Based)

Count overlapping meetings using start/end events.

```python
def min_meeting_rooms_sweep(intervals: list[list[int]]) -> int:
    """
    Find minimum rooms using sweep line algorithm.

    Create events for start (+1) and end (-1) times.
    Track maximum concurrent meetings.

    Time: O(n log n)
    Space: O(n) for events
    """
    if not intervals:
        return 0

    events = []

    for start, end in intervals:
        events.append((start, 1))   # Meeting starts
        events.append((end, -1))    # Meeting ends

    # Sort: by time, then by type (end before start at same time)
    events.sort(key=lambda x: (x[0], x[1]))

    rooms = 0
    max_rooms = 0

    for time, delta in events:
        rooms += delta
        max_rooms = max(max_rooms, rooms)

    return max_rooms
```

### Visual Trace

```
Intervals: [[0,30], [5,10], [15,20]]

Events:
(0, +1)   meeting starts
(5, +1)   meeting starts
(10, -1)  meeting ends
(15, +1)  meeting starts
(20, -1)  meeting ends
(30, -1)  meeting ends

Sorted: [(0,1), (5,1), (10,-1), (15,1), (20,-1), (30,-1)]

Processing:
t=0:  rooms=1, max=1
t=5:  rooms=2, max=2
t=10: rooms=1, max=2
t=15: rooms=2, max=2
t=20: rooms=1, max=2
t=30: rooms=0, max=2

Answer: 2
```

---

## Approach 3: Two Arrays

Separate start and end times, use two pointers.

```python
def min_meeting_rooms_two_pointers(intervals: list[list[int]]) -> int:
    """
    Find minimum rooms using sorted start/end arrays.

    Time: O(n log n)
    Space: O(n)
    """
    if not intervals:
        return 0

    starts = sorted([i[0] for i in intervals])
    ends = sorted([i[1] for i in intervals])

    rooms = 0
    end_ptr = 0

    for start in starts:
        if start >= ends[end_ptr]:
            # A meeting has ended, reuse room
            end_ptr += 1
        else:
            # Need new room
            rooms += 1

    return rooms
```

### Visual Trace

```
Intervals: [[0,30], [5,10], [15,20]]

starts = [0, 5, 15]
ends   = [10, 20, 30]

Process:
start=0:  0 < 10, need new room, rooms=1
start=5:  5 < 10, need new room, rooms=2
start=15: 15 >= 10, reuse room, end_ptr=1

Answer: 2
```

---

## Approach Comparison

| Approach     | Time       | Space | When to Use                     |
| ------------ | ---------- | ----- | ------------------------------- |
| Min-Heap     | O(n log n) | O(n)  | Most intuitive for interviews   |
| Sweep Line   | O(n log n) | O(n)  | When counting concurrent events |
| Two Pointers | O(n log n) | O(n)  | Clean, easy to remember         |

---

## Maximum Overlap at Any Point

Related: Find the maximum number of overlapping intervals at any time.

```python
def max_overlap(intervals: list[list[int]]) -> int:
    """
    Find maximum overlapping intervals at any point.
    Same as minimum meeting rooms!

    Time: O(n log n)
    Space: O(n)
    """
    events = []
    for start, end in intervals:
        events.append((start, 1))
        events.append((end, -1))

    events.sort(key=lambda x: (x[0], x[1]))

    current = 0
    maximum = 0

    for _, delta in events:
        current += delta
        maximum = max(maximum, current)

    return maximum
```

---

## Car Pooling (Variation)

Determine if a car with capacity can complete all trips.

```python
def car_pooling(trips: list[list[int]], capacity: int) -> bool:
    """
    trips[i] = [num_passengers, from, to]
    Check if all passengers can be picked up.

    Time: O(n log n) or O(max_location) with bucket sort
    Space: O(n) or O(max_location)
    """
    events = []

    for passengers, start, end in trips:
        events.append((start, passengers))    # Pick up
        events.append((end, -passengers))     # Drop off

    events.sort(key=lambda x: (x[0], x[1]))

    current_passengers = 0

    for _, change in events:
        current_passengers += change
        if current_passengers > capacity:
            return False

    return True


def car_pooling_bucket(trips: list[list[int]], capacity: int) -> bool:
    """
    Optimized for small location range using bucket sort.

    Time: O(n + max_location)
    Space: O(max_location)
    """
    max_location = max(trip[2] for trip in trips)
    delta = [0] * (max_location + 1)

    for passengers, start, end in trips:
        delta[start] += passengers
        delta[end] -= passengers

    current = 0
    for change in delta:
        current += change
        if current > capacity:
            return False

    return True
```

---

## Find Right Interval

For each interval, find the smallest start >= current end.

```python
import bisect

def find_right_interval(intervals: list[list[int]]) -> list[int]:
    """
    For each interval, find minimum j where intervals[j].start >= intervals[i].end.
    Return -1 if no such interval exists.

    Time: O(n log n)
    Space: O(n)
    """
    n = len(intervals)
    # Store (start, original_index) sorted by start
    starts = sorted((interval[0], i) for i, interval in enumerate(intervals))

    result = []
    for interval in intervals:
        end = interval[1]
        # Binary search for smallest start >= end
        idx = bisect.bisect_left(starts, (end, -1))
        if idx < n:
            result.append(starts[idx][1])
        else:
            result.append(-1)

    return result
```

---

## Complexity Analysis

| Problem                  | Time       | Space | Notes                |
| ------------------------ | ---------- | ----- | -------------------- |
| Meeting Rooms I          | O(n log n) | O(1)  | Simple overlap check |
| Meeting Rooms II (heap)  | O(n log n) | O(n)  | Heap size = rooms    |
| Meeting Rooms II (sweep) | O(n log n) | O(n)  | Event processing     |
| Car Pooling              | O(n log n) | O(n)  | Sweep line variant   |
| Car Pooling (bucket)     | O(n + k)   | O(k)  | k = max location     |

---

## Edge Cases

- [ ] Empty input → return 0 (rooms) or true (can attend)
- [ ] Single meeting → return 1 room, can attend
- [ ] All same time → return n rooms
- [ ] Sequential non-overlapping → return 1 room
- [ ] End equals start → clarify if overlap

---

## Event Sorting Tie-Breaking

**Critical for correctness**:

```
Events at same time - which to process first?

Meeting ends at 10, another starts at 10:
- If end processed first: room freed, reused → 1 room
- If start processed first: need new room → 2 rooms

Typically: ends process before starts at same time
Sort key: (time, delta) where end=-1 < start=+1
```

---

## Practice Problems

| #   | Problem          | Difficulty | Key Insight                  |
| --- | ---------------- | ---------- | ---------------------------- |
| 1   | Meeting Rooms    | Easy       | Sort, check adjacent overlap |
| 2   | Meeting Rooms II | Medium     | Min-heap or sweep line       |
| 3   | Car Pooling      | Medium     | Sweep line with capacity     |
| 4   | My Calendar I    | Medium     | Interval insertion/overlap   |
| 5   | My Calendar II   | Medium     | Track double bookings        |
| 6   | My Calendar III  | Hard       | Sweep line, max overlap      |

---

## Interview Tips

1. **Clarify overlap definition**: end=10, start=10 overlap?
2. **Choose your approach**: heap is most intuitive to explain
3. **Trace an example**: show heap operations step by step
4. **Mention alternatives**: "I could also use sweep line"
5. **Handle edge cases**: empty input, single meeting

---

## Key Takeaways

1. Meeting Rooms I: sort and check adjacent intervals
2. Meeting Rooms II: min-heap of end times or sweep line
3. Sweep line: events sorted, track concurrent count
4. Tie-breaking matters: ends before starts at same time
5. Car pooling = meeting rooms with weighted passengers

---

## Next: [05-jump-game.md](./05-jump-game.md)

Learn the jump game pattern - tracking reachability with greedy.
