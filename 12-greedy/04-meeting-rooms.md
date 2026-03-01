# Meeting Rooms

> **Prerequisites:** [Merge Intervals](./03-merge-intervals.md)

## Interview Context

Meeting rooms problems test:

1. **Interval overlap detection**: Can all meetings fit in one room?
2. **Resource allocation**: Minimum rooms needed
3. **Algorithm selection**: Sorting vs heap vs sweep line
4. **Multiple valid approaches**: Recognizing equivalent formulations

---

## Building Intuition

### Two Distinct Questions

Meeting room problems come in two flavors. Recognizing which one you are solving
determines the entire approach:

| Question | Output | Core technique |
| --- | --- | --- |
| **Can attend all meetings?** (Meeting Rooms I) | `bool` | Sort by start, check adjacent pairs |
| **Minimum rooms needed?** (Meeting Rooms II) | `int` | Track peak concurrency (heap, sweep line, or two pointers) |

### Meeting Rooms I: The "One Room" Question

Can all meetings fit in a single room? Equivalently: do any meetings overlap?

If we lay all meetings on a timeline, any "stacking" means we need more than one room:

```
Meetings: [0,30], [5,10], [15,20]

Timeline:
0----5----10---15---20---25---30
|============================|     [0,30]
     |===|                        [5,10]
               |=====|            [15,20]
     ^
     Overlap! Can't attend all in one room.
```

### Meeting Rooms II: The "Peak Concurrency" Question

How many meetings overlap at the worst moment? That peak is the minimum number of rooms.

Mental model -- a graph of "meetings in progress" over time:

```
Time:     0   5   10  15  20  25  30
Active:   1   2    1   2   1   1   0
              ^         ^
           Peak = 2 rooms needed
```

### The Three Equivalent Views

Meeting Rooms II can be solved three ways, all giving the same answer:

1. **Min-Heap (Greedy Room Reuse)**:
   - Track when each room becomes free (heap of end times)
   - For each new meeting: reuse the earliest-freeing room if possible
   - Otherwise, allocate a new room
   - Heap size = rooms in use

2. **Sweep Line (Event Counting)**:
   - +1 at each meeting start, -1 at each meeting end
   - Maximum running sum = answer

3. **Two Arrays (Sorted Starts/Ends)**:
   - Sort start times and end times independently
   - Two-pointer walk counting active meetings
   - Works because we only need the count, not which meeting pairs with which room

---

## The Interval Partitioning Theorem

**Theorem:** The minimum number of rooms needed equals the maximum number of
overlapping intervals at any point in time.

This is also called the **depth** of the interval set. All three approaches
for Meeting Rooms II compute this depth differently:

| Approach   | How It Computes Depth                                      |
| ---------- | ---------------------------------------------------------- |
| Min-Heap   | Tracks active intervals; heap size = concurrent meetings   |
| Sweep Line | Running sum of +1/-1 events; peak = max overlap            |
| Two Arrays | Two-pointer chronological sweep; peak = max active         |

**Why Greedy Works:** By processing meetings in start-time order and always
reusing the earliest-available room, we never use more rooms than necessary.
This is a classic greedy algorithm with the **greedy stays ahead** property:
at each step, we make the locally optimal choice that leads to a globally
optimal solution.

---

## When NOT to Use These Approaches

**1. When Rooms Have Different Capacities**

If rooms have size limits (room A fits 10 people, room B fits 50),
this becomes a bin packing / assignment problem, typically solved with
greedy heuristics or optimization.

**2. When Meetings Have Preferences**

If some meetings must be in specific rooms, or some rooms are preferred,
this becomes a constrained assignment problem (matching algorithms or
constraint satisfaction).

**3. When You Need the Actual Schedule**

If you need to output "meeting X goes to room Y":
- The heap approach naturally provides this: each pop/push represents a room assignment.
- The sweep line and two-array approaches only give the count, not assignments.

**4. When Intervals Can Be Rescheduled**

If you can move meetings to minimize rooms, that's a job scheduling problem with
flexibility -- much harder. These algorithms assume fixed meeting times.

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

    Overlap definition: [0,10] and [10,20] do NOT overlap (end == start is OK).
    We use strict inequality (<) to detect conflicts.

    Time:  O(n log n) for sorting
    Space: O(n) for sorting (Timsort in Python)
    """
    if len(intervals) <= 1:
        return True

    intervals = sorted(intervals, key=lambda x: x[0])

    for i in range(1, len(intervals)):
        # If current meeting starts before previous ends -> conflict
        # Note: start == previous end is NOT a conflict (back-to-back OK)
        if intervals[i][0] < intervals[i - 1][1]:
            return False

    return True
```

### Visual Trace

```
Intervals: [[0,30], [5,10], [15,20]]

After sort by start: [[0,30], [5,10], [15,20]]  (already sorted)

Timeline:
[0,30]:  |------------------------------|
[5,10]:      |-----|
[15,20]:               |-----|

Check adjacent pairs:
  i=1: [5,10].start = 5 < 30 = [0,30].end  --> CONFLICT --> return False
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

Track the end times of ongoing meetings in a min-heap. The heap's minimum tells us
when the earliest room becomes free.

**Intuition:** Each entry in the heap represents one room currently in use. The
heap value is when that room becomes available. When a new meeting arrives, if
the earliest-freeing room is free (its end time <= new meeting's start), we reuse
it by popping the old end time and pushing the new one. Otherwise we allocate a
new room by pushing without popping.

```python
import heapq

def min_meeting_rooms(intervals: list[list[int]]) -> int:
    """
    Find minimum meeting rooms needed using a min-heap.

    Strategy: For each meeting (sorted by start time), check if the
    earliest-ending room is free. If so, reuse it (pop + push).
    Otherwise, allocate a new room (push only).

    The heap size at any point = number of rooms currently in use.

    Time:  O(n log n) -- sorting dominates; each heap op is O(log n)
    Space: O(n) for heap
    """
    if not intervals:
        return 0

    intervals = sorted(intervals, key=lambda x: x[0])

    # Min-heap of end times (each entry = one room in use)
    heap = [intervals[0][1]]

    for start, end in intervals[1:]:
        # Earliest-ending room is free -> reuse it
        if start >= heap[0]:
            heapq.heappop(heap)

        # Push current meeting's end time
        # (reuse case: replaces old end; new room case: adds a room)
        heapq.heappush(heap, end)

    return len(heap)
```

### Visual Trace

```
Intervals: [[0,30], [5,10], [15,20]]
Sorted:    [[0,30], [5,10], [15,20]]  (already sorted)

Step 1: Process [0,30]
  Initialize heap with first meeting's end time
  heap = [30]                            --> 1 room in use

Step 2: Process [5,10]
  start=5 < heap[0]=30  --> room not free, allocate new room
  heap = [10, 30]                        --> 2 rooms in use

Step 3: Process [15,20]
  start=15 >= heap[0]=10  --> room is free! Pop 10, push 20
  heap = [20, 30]                        --> 2 rooms in use (reused)

Answer: len(heap) = 2
```

**Larger example** to show heap dynamics more clearly:

```
Intervals (sorted): [[1,5], [2,6], [4,8], [6,9], [7,10]]

Step 1: [1,5]   heap = [5]                 rooms = 1
Step 2: [2,6]   2 < 5  -> new room         heap = [5, 6]       rooms = 2
Step 3: [4,8]   4 < 5  -> new room         heap = [5, 6, 8]    rooms = 3
Step 4: [6,9]   6 >= 5 -> reuse (pop 5)    heap = [6, 8, 9]    rooms = 3
Step 5: [7,10]  7 >= 6 -> reuse (pop 6)    heap = [8, 9, 10]   rooms = 3

Answer: 3

Timeline visualization:
Room 1: [1-----5]         [6-------9]
Room 2:   [2-------6]       [7--------10]
Room 3:       [4---------8]
```

---

## Approach 2: Sweep Line (Event-Based)

Convert intervals into discrete events (start = +1, end = -1), then sweep through
time tracking the running sum. The maximum running sum is the answer.

```python
def min_meeting_rooms_sweep(intervals: list[list[int]]) -> int:
    """
    Find minimum rooms using sweep line algorithm.

    Create +1 (start) and -1 (end) events, sort them, and track the
    running count of active meetings. The peak count = rooms needed.

    Tie-breaking: at the same time, process ends (-1) before starts (+1).
    This ensures that a room freed at time t can be reused at time t.
    Sorting by (time, delta) handles this automatically since -1 < +1.

    Time:  O(n log n)
    Space: O(n) for events
    """
    if not intervals:
        return 0

    events = []
    for start, end in intervals:
        events.append((start, 1))   # meeting starts
        events.append((end, -1))    # meeting ends

    # Sort by time, then by delta (ends before starts at same time)
    events = sorted(events)

    active = 0
    max_active = 0

    for _, delta in events:
        active += delta
        max_active = max(max_active, active)

    return max_active
```

### Visual Trace

```
Intervals: [[0,30], [5,10], [15,20]]

Events (sorted):
(0,  +1)  start
(5,  +1)  start
(10, -1)  end
(15, +1)  start
(20, -1)  end
(30, -1)  end

Processing:
t=0:  active = 0+1 = 1, max = 1
t=5:  active = 1+1 = 2, max = 2   <-- peak
t=10: active = 2-1 = 1, max = 2
t=15: active = 1+1 = 2, max = 2   <-- ties peak
t=20: active = 2-1 = 1, max = 2
t=30: active = 1-1 = 0, max = 2

Answer: 2
```

---

## Approach 3: Two Arrays (Sorted Starts/Ends)

Sort start times and end times independently, then use two pointers. This works
because we only care about _how many_ meetings are active, not _which_ meeting
ends correspond to which starts. Sorting breaks the pairing, but the count is
preserved.

**Why This Works:** We process meetings in start-time order. For each meeting,
we check if the earliest-ending meeting has finished (`start >= ends[end_ptr]`).
If yes, we reuse that room (advance `end_ptr`). If no, we need a new room.
The key insight: `rooms` counts how many times we couldn't reuse a room, which
equals `n - end_ptr` at the end -- the minimum rooms needed.

```python
def min_meeting_rooms_two_pointers(intervals: list[list[int]]) -> int:
    """
    Find minimum rooms using sorted start/end arrays with two pointers.

    Key insight: We track the number of active meetings.
    By sorting starts and ends independently, we can sweep through time.
    If the next event is a start, active rooms increase.
    If the next event is an end, active rooms decrease.
    The maximum active rooms at any point is our answer.

    Time:  O(n log n) for sorting
    Space: O(n) for start/end arrays
    """
    if not intervals:
        return 0

    starts = sorted(i[0] for i in intervals)
    ends = sorted(i[1] for i in intervals)

    active_rooms = 0
    max_rooms = 0
    s_ptr = 0
    e_ptr = 0
    n = len(intervals)

    while s_ptr < n:
        # If the next meeting starts before the earliest ending meeting finishes,
        # we have a new concurrent meeting (need another room).
        if starts[s_ptr] < ends[e_ptr]:
            active_rooms += 1
            max_rooms = max(max_rooms, active_rooms)
            s_ptr += 1
        else:
            # A meeting finished, so a room is freed.
            active_rooms -= 1
            e_ptr += 1

    return max_rooms
```

### Visual Trace

```
Intervals: [[0,30], [5,10], [15,20]]

starts = [0, 5, 15]
ends   = [10, 20, 30]

Process with pointers (s_ptr, e_ptr):
s_ptr=0, e_ptr=0: starts[0]=0 < ends[0]=10    -> active=1, max=1, s_ptr=1
s_ptr=1, e_ptr=0: starts[1]=5 < ends[0]=10    -> active=2, max=2, s_ptr=2
s_ptr=2, e_ptr=0: starts[2]=15 >= ends[0]=10  -> active=1, max=2, e_ptr=1
s_ptr=2, e_ptr=1: starts[2]=15 < ends[1]=20   -> active=2, max=2, s_ptr=3
(loop terminates since s_ptr == n)

Answer: 2

Why does separating starts/ends work?
We don't care WHICH meeting ended -- just that SOME meeting ended by
the time the next one starts. The sorted order preserves this count.
```

---

## Approach Comparison

| Approach     | Time         | Space  | Strengths                                 |
| ------------ | ------------ | ------ | ----------------------------------------- |
| Min-Heap     | $O(n \log n)$ | $O(n)$ | Gives room assignments, most intuitive    |
| Sweep Line   | $O(n \log n)$ | $O(n)$ | Generalizes to weighted events (car pool) |
| Two Arrays   | $O(n \log n)$ | $O(n)$ | Simplest code, easiest to remember        |

---

## Event Sorting Tie-Breaking

**Critical for correctness** in the sweep line approach:

```
Meeting A ends at 10, meeting B starts at 10.
Should they need 1 room or 2?

Convention: [0,10] and [10,20] do NOT overlap.
A room freed at time 10 can be reused at time 10.

--> Process ends before starts at the same time.

This happens automatically when sorting (time, delta) tuples:
  (10, -1) sorts before (10, +1) because -1 < +1.
```

For the heap and two-array approaches, the equivalent logic is the `<` versus `>=`
comparison: `start < end` means conflict, while `start >= end` means reuse is allowed.

---

## Practice Problem 1: Car Pooling (LC 1094)

### Problem Statement

A vehicle has a given `capacity`. You are given `trips` where
`trips[i] = [num_passengers, from, to]`. Return whether the vehicle can
complete all trips without exceeding capacity at any point.

This is Meeting Rooms II with _weighted_ events: instead of +1/-1 per meeting,
we add/subtract the number of passengers.

### Solution: Sweep Line

```python
def car_pooling(trips: list[list[int]], capacity: int) -> bool:
    """
    Check if all trips can be completed without exceeding capacity.

    Tie-breaking: at the same location, drop-offs (-passengers) must be
    processed before pick-ups (+passengers) to avoid false capacity violations.
    Python tuple sorting handles this: (10, -5) < (10, 5) because -5 < 5.

    Time:  O(n log n)
    Space: O(n)
    """
    events = []
    for passengers, start, end in trips:
        events.append((start, passengers))    # pick up
        events.append((end, -passengers))     # drop off

    events = sorted(events)

    current_passengers = 0
    for _, change in events:
        current_passengers += change
        if current_passengers > capacity:
            return False

    return True
```

### Solution: Difference Array (Bucket Sort)

When the location range is small (the problem constrains locations to
`0 <= from < to <= 1000`), a difference array avoids sorting entirely:

```python
def car_pooling_bucket(trips: list[list[int]], capacity: int) -> bool:
    """
    Optimized for small location range using a difference array.

    Time:  O(n + k) where k = max location
    Space: O(k)
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

### Visual Trace

```
trips = [[2, 1, 5], [3, 3, 7], [1, 5, 8]], capacity = 4

Events (before sort):
  (1, +2), (5, -2)   # trip 1: 2 passengers from loc 1 to 5
  (3, +3), (7, -3)   # trip 2: 3 passengers from loc 3 to 7
  (5, +1), (8, -1)   # trip 3: 1 passenger  from loc 5 to 8

Events (sorted -- note tie-breaking at location 5):
  (1, +2), (3, +3), (5, -2), (5, +1), (7, -3), (8, -1)
                         ^ drop-off before pick-up

Processing:
  loc=1: current = 0 + 2 = 2   (capacity 4: OK)
  loc=3: current = 2 + 3 = 5   (capacity 4: EXCEEDS!) --> return False

With capacity = 5:
  loc=1: current = 0 + 2 = 2   OK
  loc=3: current = 2 + 3 = 5   OK (at capacity)
  loc=5: current = 5 - 2 = 3   (drop off 2)
         current = 3 + 1 = 4   (pick up 1) OK
  loc=7: current = 4 - 3 = 1   OK
  loc=8: current = 1 - 1 = 0   all dropped off
  --> return True
```

---

## Practice Problem 2: My Calendar I & II (LC 729, 731)

### Problem Statement

Implement a calendar system to store events and check for conflicts:
- **My Calendar I**: Prevent any double booking.
- **My Calendar II**: Allow double booking, but prevent triple booking.

These problems test the ability to dynamically check overlaps as events are added.

### Solution: My Calendar I

For a few events, we can just check against all existing events. For $O(\log n)$ per booking, we could use a balanced Binary Search Tree (like `SortedDict` in Python or `std::set` in C++), but $O(n)$ is often sufficient.

```python
class MyCalendar:
    """
    LeetCode 729: Prevent double booking.

    Time:  O(n) per book(), O(n^2) total
    Space: O(n) for the calendar array
    """
    def __init__(self):
        self.calendar = []

    def book(self, start: int, end: int) -> bool:
        for s, e in self.calendar:
            # Overlap condition: max(start1, start2) < min(end1, end2)
            # Or simpler: new starts before old ends AND old starts before new ends
            if start < e and s < end:
                return False

        self.calendar.append((start, end))
        return True
```

### Solution: My Calendar II

To prevent triple bookings, we can maintain two lists: one for all events, and one for the regions that are double-booked. When a new event arrives, we first check if it overlaps with any double-booked region.

```python
class MyCalendarTwo:
    """
    LeetCode 731: Prevent triple booking.

    Time:  O(n) per book()
    Space: O(n) for calendar and overlaps arrays
    """
    def __init__(self):
        self.calendar = []
        self.overlaps = []

    def book(self, start: int, end: int) -> bool:
        # 1. Check if it causes a triple booking
        for s, e in self.overlaps:
            if start < e and s < end:
                return False

        # 2. Add to overlaps where it intersects with existing events
        for s, e in self.calendar:
            if start < e and s < end:
                self.overlaps.append((max(start, s), min(end, e)))

        # 3. Add to calendar
        self.calendar.append((start, end))
        return True
```

This leads naturally into **My Calendar III (LC 732)**, where we want to find the maximum k-booking. This is exactly the Sweep Line approach from Meeting Rooms II, run dynamically on every insertion (using a dictionary to accumulate `+1` / `-1` deltas).

---

## Practice Problem 3: Minimum Number of Arrows to Burst Balloons (LC 452)

### Problem Statement

Balloons are represented as intervals `[x_start, x_end]` on the x-axis. An arrow
shot at position `x` bursts all balloons where `x_start <= x <= x_end`. Find the
minimum number of arrows needed to burst all balloons.

This is the **complement of interval scheduling**: instead of finding the maximum
non-overlapping intervals, we find the minimum number of "groups" of overlapping
intervals (each group can be burst by one arrow).

### Solution

```python
def find_min_arrow_shots(points: list[list[int]]) -> int:
    """
    Minimum arrows to burst all balloons.

    Greedy: sort by end position. Shoot an arrow at each balloon's end.
    This arrow bursts all balloons that overlap with the current one.
    Skip balloons already burst, and shoot again when we find one that isn't.

    This is equivalent to: "maximum number of non-overlapping intervals"
    tells us how many arrows we need (each arrow handles one cluster).

    Time:  O(n log n) for sorting
    Space: O(n) for sorting
    """
    if not points:
        return 0

    # Sort by end position (same logic as interval scheduling)
    points = sorted(points, key=lambda x: x[1])

    arrows = 1
    arrow_pos = points[0][1]  # shoot at first balloon's end

    for start, end in points[1:]:
        if start > arrow_pos:
            # This balloon isn't burst by current arrow -- need a new one
            arrows += 1
            arrow_pos = end

    return arrows
```

### Visual Trace

```
Balloons: [[10,16], [2,8], [1,6], [7,12]]

Sorted by end: [[1,6], [2,8], [7,12], [10,16]]

Step 1: [1,6]   Shoot arrow at x=6.  arrows=1, arrow_pos=6
Step 2: [2,8]   start=2 <= 6  --> burst by current arrow (skip)
Step 3: [7,12]  start=7 > 6   --> need new arrow at x=12.  arrows=2, arrow_pos=12
Step 4: [10,16] start=10 <= 12 --> burst by current arrow (skip)

Answer: 2

Timeline:
  [1------6]         <-- arrow at x=6 bursts this
    [2--------8]     <-- also burst by arrow at x=6
         [7------12] <-- arrow at x=12 bursts this
            [10------16]  <-- also burst by arrow at x=12
       ^              ^
    arrow 1        arrow 2
```

**Connection to Meeting Rooms:** Balloons = meetings, arrows = rooms. The minimum
arrows equals the minimum "groups" that cover all intervals, which is the depth
of the interval set (same as Meeting Rooms II) when intervals are allowed to touch.
Note the subtle difference: here `start > arrow_pos` (strict inequality) because
touching at a single point counts as overlapping for balloon bursting.

---

## Complexity Summary

| Problem                  | Time            | Space    | Notes                    |
| ------------------------ | --------------- | -------- | ------------------------ |
| Meeting Rooms I          | $O(n \log n)$   | $O(n)^*$ | Simple overlap check     |
| Meeting Rooms II (heap)  | $O(n \log n)$   | $O(n)$   | Heap size = rooms        |
| Meeting Rooms II (sweep) | $O(n \log n)$   | $O(n)$   | Event processing         |
| Car Pooling              | $O(n \log n)$   | $O(n)$   | Sweep line variant       |
| Car Pooling (bucket)     | $O(n + k)$      | $O(k)$   | k = max location         |
| My Calendar I / II       | $O(n)$          | $O(n)$   | Per `book()` operation   |
| Burst Balloons (arrows)  | $O(n \log n)$   | $O(n)$   | Sort by end, greedy scan |

$^*O(n)$ space is required in Python because `sorted()` creates a new list and Timsort uses $O(n)$ worst-case memory. In languages with in-place sorting (like C++ `std::sort`), it can be $O(1)$ or $O(\log n)$ depending on the algorithm.

---

## Edge Cases

- **Empty input**: return 0 rooms or `True` (can attend)
- **Single meeting**: 1 room needed, can attend
- **All meetings at the same time**: need $n$ rooms
- **Sequential, non-overlapping**: need 1 room
- **End equals next start** (e.g., `[0,10]` and `[10,20]`): NOT overlapping in the standard convention. All three approaches handle this correctly: the heap and two-array approaches use `<` vs `>=` for reuse, and the sweep line processes ends before starts at the same time
- **Zero-duration meetings** (e.g., `[5,5]`): Edge case that depends on the problem definition. Typically they don't conflict with anything
- **Large coordinate values**: Algorithms work with any integer values; only relative ordering matters

---

## Interview Tips

1. **Clarify overlap definition**: Does `end=10, start=10` count as overlapping? (Usually no -- back-to-back meetings are allowed.)
2. **Pick one approach and explain it well**: The heap approach is the most intuitive to walk through and provides room assignments.
3. **Trace a small example**: Show the heap operations or event processing step by step. Draw the timeline.
4. **Mention alternatives**: "I could also solve this with a sweep line or two-pointer approach, all with the same $O(n \log n)$ complexity."
5. **Handle edge cases explicitly**: Empty input, single meeting, all-overlapping, touching intervals.
6. **Explain the greedy choice**: Why does reusing the earliest-ending room work? Because it leaves maximum flexibility for future meetings.
7. **For follow-ups**: Be ready to extend to room assignments (heap), weighted intervals (car pooling), or dynamic scheduling.

---

## Key Takeaways

1. **Meeting Rooms I vs II**: I = "do any overlap?" (bool). II = "what is the peak overlap?" (int). Completely different algorithms.
2. **Meeting Rooms II**: Three equivalent approaches -- min-heap, sweep line, or two-pointer -- all $O(n \log n)$
3. **Interval Partitioning Theorem**: Minimum rooms = maximum overlapping intervals at any point (the "depth")
4. **Min-heap intuition**: Each heap entry is a room; the value is when it becomes free. Pop = reuse room. Push without pop = new room.
5. **Sweep line**: Events sorted by (time, delta); max running sum = answer; generalizes to weighted problems like car pooling
6. **Tie-breaking matters**: Ends before starts at the same time (delta -1 < +1); equivalent to `>=` in heap/two-pointer
7. **Two-pointer insight**: Sorting breaks interval pairing but preserves the count -- we only need the count
8. **Room assignments**: Only the heap approach tracks which meeting goes to which room
9. **Greedy stays ahead**: Reusing the earliest-ending room leaves maximum flexibility for future meetings

---

## Next: [05-jump-game.md](./05-jump-game.md)

Learn the jump game pattern -- tracking reachability with greedy.
