# Difference Array

> **Prerequisites:** [06-prefix-sum.md](./06-prefix-sum.md)

## Overview

Difference arrays are the inverse of prefix sums. While prefix sums enable $\Theta(1)$ range queries (after $\Theta(n)$ preprocessing), difference arrays enable $\Theta(1)$ range updates. This makes them ideal for batch update scenarios where you modify many ranges before needing the final values.

## Building Intuition

**Why does marking just two positions update an entire range?**

The key insight is **deferred computation**. Instead of updating every element in a range, we record where changes start and stop:

1. **The "Delta" Concept**: A difference array stores changes between consecutive elements. Adding `v` to range `[i, j]` means:
   - At position `i`: values start being `v` more than before.
   - At position `j + 1`: values stop being `v` more than before.
   - Only these two boundaries matter!

2. **Reconstruction via Prefix Sum**: When we need actual values, we compute prefix sums of the difference array. Each position accumulates all the "start adding" signals minus all the "stop adding" signals up to that point.

3. **The Event Model**: Think of `diff[i]` as "at position `i`, increase all future values by this amount." Adding at the start and subtracting after the end creates a pulse that spans exactly `[i, j]`.

**Physical Metaphor**: Imagine you're managing a concert venue with a long hallway of numbered sections. Instead of sending a worker to add 3 chairs to every section from 5 to 20, you put a sticky note at section 5 saying "+3 chairs starting here" and another at section 21 saying "-3 chairs starting here". At the end of the day, a single worker walks the hallway, keeping a running total of the sticky notes and updating the actual chair counts in one pass.

**Visual Trace**:

```text
Range update: add 3 to indices [1, 4]
              add 2 to indices [2, 3]

Difference array operations:
Initial:  [0, 0, 0, 0, 0, 0]
After +3 to [1,4]:
          [0, +3, 0, 0, 0, -3]
After +2 to [2,3]:
          [0, +3, +2, 0, -2, -3]

Prefix sum to reconstruct:
Position: 0   1   2   3   4   5
Diff:     0   3   2   0  -2  -3
Prefix:   0   3   5   5   3   0
          ↑   ↑   ↑   ↑   ↑   ↑
          base +3  +5  +5  +3  back to 0
```

## When NOT to Use Difference Arrays

Difference arrays have specific requirements:

1. **Queries Interleaved with Updates**: If you need to query the array value between updates, you must rebuild ($\Theta(n)$) each time. For interleaved update/query, use segment trees or binary indexed trees (Fenwick trees).
2. **Point Updates, Not Range Updates**: If you're updating single elements (not ranges), difference arrays add complexity without benefit. Just update directly.
3. **Large Sparse Ranges**: If the array is huge but updates are sparse and don't overlap much, using a list of `(start, end, value)` tuples or a hash map (remembering hash map lookups are amortized $\Theta(1)$ but worst-case $O(n)$) may be simpler.
4. **When You Need Original Values Preserved**: Difference arrays typically overwrite the original or require an extra array. If you need both original and modified concurrently without extra space, this technique isn't magical.
5. **Non-Additive Operations**: Difference arrays work perfectly for additive updates. For "set range to value" or "multiply range by x," you need different techniques like segment trees with lazy propagation.

**Red Flags:**
- "Query between updates" $\rightarrow$ Segment tree / Fenwick tree
- "Update single elements" $\rightarrow$ Direct modification
- "Set range to value" (not add) $\rightarrow$ Segment tree with lazy propagation

---

## Core Concept

A difference array stores the difference between consecutive elements:

```text
Original:    [1, 3, 6, 10, 15]
Difference:  [1, 2, 3, 4, 5]

diff[0] = arr[0]
diff[i] = arr[i] - arr[i-1]

To recover original: compute the prefix sum of the difference array.
```

### Key Property

To add value `v` to range `[i, j]`:

- Add `v` to `diff[i]` (start adding)
- Subtract `v` from `diff[j+1]` (stop adding)

After all updates, reconstruct the array with a prefix sum pass.

---

## Template: Range Addition

### Problem: Range Addition

**Problem Statement:** You are given an integer `length` and a 2D array `updates` where `updates[i] = [start_i, end_i, inc_i]`. Increment each element of the array in the range `[start_i, end_i]` by `inc_i` and return the final array.

**Why it works:**
Updating a range `[L, R]` with value `v` in a difference array `D` involves only two operations: `D[L] += v` and `D[R+1] -= v`.
1. The difference array `D` represents the change between adjacent elements.
2. Increasing `D[L]` means every element from `L` onwards in the reconstructed array will be increased by `v`.
3. Decreasing `D[R+1]` cancels out that increase for all elements from `R+1` onwards.
This turns $\Theta(k \cdot n)$ range updates into $\Theta(k)$ point updates followed by a single $\Theta(n)$ prefix sum pass.

```python
def range_addition(length: int, updates: list[list[int]]) -> list[int]:
    """
    Apply multiple range additions and return the final array.

    Updates format: [[start, end, value], ...]

    Time Complexity: \Theta(n + k) where n = length, k = len(updates)
    Space Complexity: \Theta(n) for the difference array/result array
    """
    # Pre-allocate the exact size needed, which is \Theta(n) space.
    diff: list[int] = [0] * (length + 1)  # Extra element for end + 1

    # Apply all updates to difference array
    for start, end, val in updates:
        diff[start] += val
        diff[end + 1] -= val

    # Reconstruct with prefix sum
    result: list[int] = [0] * length
    current = 0
    for i in range(length):
        current += diff[i]
        result[i] = current

    return result
```

### Visual Trace

```text
length = 5, updates = [[1,3,2], [2,4,3], [0,2,-2]]

Initial diff: [0, 0, 0, 0, 0, 0]

After [1,3,2] (add 2 to indices 1-3):
diff: [0, 2, 0, 0, -2, 0]
       ↑     ↑        ↑
       |     add 2    stop at 4

After [2,4,3] (add 3 to indices 2-4):
diff: [0, 2, 3, 0, -2, -3]

After [0,2,-2] (add -2 to indices 0-2):
diff: [-2, 2, 3, 2, -2, -3]

Prefix sum reconstruction:
i=0: current = -2       result[0] = -2
i=1: current = -2+2 = 0 result[1] = 0
i=2: current = 0+3 = 3  result[2] = 3
i=3: current = 3+2 = 5  result[3] = 5
i=4: current = 5-2 = 3  result[4] = 3

Final: [-2, 0, 3, 5, 3]
```

---

## Template: Car Pooling

### Problem: Car Pooling

**Problem Statement:** There is a vehicle with `capacity` empty seats. Given a list of `trips` where `trips[i] = [num_passengers, start_location, end_location]`, return `True` if it is possible to pick up and drop off all passengers for all the given trips, or `False` otherwise.

**Why it works:**
The number of passengers in the car at any location `x` is the cumulative sum of all passengers who entered minus those who exited before or at `x`.
1. We use a difference array where we add `num_passengers` at `start_location` and subtract them at `end_location`.
2. We compute the prefix sum to find the passenger count at every point along the route.
3. If the count exceeds `capacity` at any point, the schedule is impossible.

```python
def car_pooling(trips: list[list[int]], capacity: int) -> bool:
    """
    Check if car can complete all trips without exceeding capacity.
    trips[i] = [num_passengers, start_location, end_location]

    Time Complexity: \Theta(n + m) where n = len(trips), m = max_location
    Space Complexity: \Theta(m) for the difference array
    """
    if not trips:
        return True

    # Find max location to size our difference array
    max_loc = max(trip[2] for trip in trips)

    # Difference array up to max_loc + 1
    diff: list[int] = [0] * (max_loc + 2)

    for passengers, start, end in trips:
        diff[start] += passengers
        diff[end] -= passengers  # Passengers get off at end (no +1 needed here)

    # Check capacity at each location
    current = 0
    for i in range(max_loc + 1):
        current += diff[i]
        if current > capacity:
            return False

    return True
```

---

## Template: Meeting Rooms II (Minimum Rooms)

### Problem: Meeting Rooms II

**Problem Statement:** Given an array of meeting time intervals `intervals` where `intervals[i] = [start_i, end_i]`, return the minimum number of conference rooms required.

**Why it works:**
The number of rooms needed at any time `t` is the number of meetings happening concurrently.
1. We mark the start of each meeting as `+1` room needed and the end as `-1` room.
2. Sorting these events by time and calculating the running sum gives us the room occupancy over time.
3. The peak value of this running sum is the minimum number of rooms needed.
This "sweep-line" approach (which is effectively using a difference array on a sorted timeline) efficiently finds the maximum concurrency.

```python
def min_meeting_rooms(intervals: list[list[int]]) -> int:
    """
    Minimum number of meeting rooms required (Difference Array approach).
    Best when max_time is relatively small.

    Time Complexity: \Theta(n + m) where n = len(intervals), m = max_time
    Space Complexity: \Theta(m) for the difference array
    """
    if not intervals:
        return 0

    max_time = max(interval[1] for interval in intervals)
    diff: list[int] = [0] * (max_time + 2)

    for start, end in intervals:
        diff[start] += 1
        diff[end] -= 1

    # Find maximum concurrent meetings
    current = 0
    max_rooms = 0
    for i in range(max_time + 1):
        current += diff[i]
        max_rooms = max(max_rooms, current)

    return max_rooms
```

### Alternative: Event-Based (More Space Efficient)

When the time range is huge (e.g., timestamps up to $10^9$) but there are few meetings, allocating a massive difference array is wasteful. Instead, we sort the endpoints.

```python
def min_meeting_rooms_events(intervals: list[list[int]]) -> int:
    """
    Using sorted events instead of a full difference array.
    Better when time range is large but intervals are few.

    Time Complexity: \Theta(n \log n) for sorting
    Space Complexity: \Theta(n) for storing the events
    """
    events: list[tuple[int, int]] = []

    for start, end in intervals:
        events.append((start, 1))   # Meeting starts
        events.append((end, -1))    # Meeting ends

    # Sort primarily by time. If times match, -1 (end) comes before 1 (start)
    # This correctly frees up a room before a new meeting tries to claim it!
    events.sort()

    current = 0
    max_rooms = 0
    for _, delta in events:
        current += delta
        max_rooms = max(max_rooms, current)

    return max_rooms
```

---

## Template: Corporate Flight Bookings

### Problem: Corporate Flight Bookings

**Problem Statement:** There are `n` flights that are labeled from `1` to `n`. You are given an array of flight bookings `bookings`, where `bookings[i] = [first_i, last_i, seats_i]` represents a booking for flights `first_i` through `last_i` with `seats_i` seats reserved for each flight in the range. Return an array `answer` of length `n` where `answer[i]` is the total number of seats reserved for flight `i`.

**Why it works:**
This is a direct application of the difference array for range updates.
1. We apply `D[first] += seats` and `D[last+1] -= seats`.
2. The final passenger count for each flight is the prefix sum of the difference array.
This handles multiple overlapping bookings in $\Theta(n + k)$ time.

```python
def corp_flight_bookings(bookings: list[list[int]], n: int) -> list[int]:
    """
    Each booking: [first, last, seats] books seats on flights first to last.
    Return total seats for each flight.

    Time Complexity: \Theta(n + k) where k = len(bookings)
    Space Complexity: \Theta(n) for the difference array/result array
    """
    # 1-indexed flights require extra space. +2 for safety with last+1
    diff: list[int] = [0] * (n + 2)

    for first, last, seats in bookings:
        diff[first] += seats
        diff[last + 1] -= seats

    result: list[int] = []
    current = 0
    for i in range(1, n + 1):
        current += diff[i]
        result.append(current)

    return result
```

---

## 2D Difference Array

For 2D range updates, we need 4 operations per update. Think of it like a 2D bounding box where you add to the top-left, but then you have to subtract from the bottom-left and top-right (to bound the box), and re-add to the bottom-right (because it was subtracted twice!).

```python
def range_addition_2d(matrix: list[list[int]],
                      updates: list[tuple[int, int, int, int, int]]) -> list[list[int]]:
    """
    Apply 2D range additions.
    updates format: [(r1, c1, r2, c2, val), ...]

    Time Complexity: \Theta(m \cdot n + k) where k = len(updates)
    Space Complexity: \Theta(m \cdot n) for the 2D difference array and result
    """
    if not matrix or not matrix[0]:
        return []

    m, n = len(matrix), len(matrix[0])
    diff = [[0] * (n + 2) for _ in range(m + 2)]

    for r1, c1, r2, c2, val in updates:
        diff[r1][c1] += val
        diff[r1][c2 + 1] -= val
        diff[r2 + 1][c1] -= val
        diff[r2 + 1][c2 + 1] += val

    # Reconstruct with 2D prefix sum
    result = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            # Accumulate exactly like a standard 2D prefix sum
            diff[i][j] += (diff[i-1][j] if i > 0 else 0)
            diff[i][j] += (diff[i][j-1] if j > 0 else 0)
            diff[i][j] -= (diff[i-1][j-1] if i > 0 and j > 0 else 0)

            result[i][j] = matrix[i][j] + diff[i][j]

    return result
```

---

## Prefix Sum vs Difference Array

| Operation    | Prefix Sum | Difference Array |
| ------------ | ---------- | ---------------- |
| Build        | $\Theta(n)$| $\Theta(n)$      |
| Range Query  | $\Theta(1)$| $\Theta(n)$      |
| Range Update | $\Theta(n)$| $\Theta(1)$      |
| Point Update | $\Theta(n)$| $\Theta(1)$      |
| Point Query  | $\Theta(1)$| $\Theta(n)$      |

**Use Prefix Sum when**: Many queries, few/no updates.
**Use Difference Array when**: Many updates, few queries.

---

## Converting Between Them

```python
def to_difference(arr: list[int]) -> list[int]:
    """Convert an original array to a difference array in \Theta(n) time/space."""
    if not arr:
        return []
    diff: list[int] = [arr[0]]
    for i in range(1, len(arr)):
        diff.append(arr[i] - arr[i-1])
    return diff

def to_original(diff: list[int]) -> list[int]:
    """Convert a difference array back to original array (Prefix sum) in \Theta(n) time/space."""
    if not diff:
        return []
    arr: list[int] = [diff[0]]
    for i in range(1, len(diff)):
        arr.append(arr[-1] + diff[i])
    return arr
```

---

## Edge Cases

```text
# Single element
[5] → diff = [5]

# Range covers entire array
update [0, n-1] → diff[0] += v, diff[n] -= v

# Adjacent updates that cancel
[[0,2,5], [0,2,-5]] → no change

# Overlapping ranges
Updates accumulate correctly

# Empty updates
Return original array
```

---

## Practice Problems

| #   | Problem                      | Difficulty | Key Concept                |
| --- | ---------------------------- | ---------- | -------------------------- |
| 1   | Range Addition               | Medium     | Basic difference array     |
| 2   | Car Pooling                  | Medium     | Capacity check             |
| 3   | Corporate Flight Bookings    | Medium     | 1-indexed bookings         |
| 4   | Meeting Rooms II             | Medium     | Maximum concurrent         |
| 5   | My Calendar III              | Hard       | Maximum overlapping events |
| 6   | Brightest Position on Street | Medium     | Light intensity            |

---

## Key Takeaways

1. **Difference array = inverse of prefix sum**.
2. **Range update in $\Theta(1)$**: add at start, subtract at end+1.
3. **Reconstruct with prefix sum** after all updates.
4. **Great for batch updates** with single reconstruction.
5. **Event-based alternative** when range is sparse (using sorting).
6. **2D version** uses 4 operations per update to form an accumulating rectangle.

---

## Next: [08-kadanes-algorithm.md](./08-kadanes-algorithm.md)

Learn Kadane's algorithm for maximum subarray problems.
