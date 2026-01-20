# Difference Array

> **Prerequisites:** [06-prefix-sum.md](./06-prefix-sum.md)

## Overview

Difference arrays are the inverse of prefix sums. While prefix sums enable O(1) range queries, difference arrays enable O(1) range updates. This makes them ideal for batch update scenarios where you modify many ranges before needing the final values.

## Building Intuition

**Why does marking just two positions update an entire range?**

The key insight is **deferred computation**. Instead of updating every element in a range, we record where changes start and stop:

1. **The "Delta" Concept**: A difference array stores changes between consecutive elements. Adding `v` to range [i, j] means:
   - At position i: values start being `v` more than before
   - At position j+1: values stop being `v` more than before
   - Only these two boundaries matter!

2. **Reconstruction via Prefix Sum**: When we need actual values, we compute prefix sums of the difference array. Each position accumulates all the "start adding" signals minus all the "stop adding" signals up to that point.

3. **The Event Model**: Think of diff[i] as "at position i, increase all future values by this amount." Adding at start, subtracting after end creates a pulse that spans exactly [i, j].

**Mental Model**: Imagine you're adjusting thermostat schedules. At 8 AM, set temperature +5°. At 5 PM, set temperature -5° (canceling the increase). During 8 AM - 5 PM, the temperature is elevated. You only set two events, not every hour individually.

**Visual Trace**:
```
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

1. **Queries Interleaved with Updates**: If you need to query the array value between updates, you must rebuild (O(n)) each time. For interleaved update/query, use segment trees with lazy propagation.

2. **Point Updates, Not Range Updates**: If you're updating single elements (not ranges), difference arrays add complexity without benefit. Just update directly.

3. **Large Sparse Ranges**: If the array is huge but updates are sparse and don't overlap much, using a list of (start, end, value) tuples may be simpler.

4. **When You Need Original Values Preserved**: Difference arrays overwrite the original. If you need both original and modified, you need extra space anyway.

5. **Non-Additive Operations**: Difference arrays work for additive updates. For "set range to value" or "multiply range by x," you need different techniques.

**Red Flags:**
- "Query between updates" → Segment tree with lazy propagation
- "Update single elements" → Direct modification
- "Set range to value" (not add) → Need different approach

---

## Interview Context

Difference arrays are the inverse of prefix sums. While prefix sums enable O(1) range queries, difference arrays enable O(1) range updates.

Common interview problems:
- Range addition queries
- Car pooling / meeting room capacity
- Flight booking problems
- Painting fences

---

## Core Concept

A difference array stores the difference between consecutive elements:

```
Original:    [1, 3, 6, 10, 15]
Difference:  [1, 2, 3, 4, 5]

diff[0] = arr[0]
diff[i] = arr[i] - arr[i-1]

To recover original: prefix sum of difference array
```

### Key Property

To add value `v` to range `[i, j]`:
- Add `v` to `diff[i]` (start adding)
- Subtract `v` from `diff[j+1]` (stop adding)

After all updates, reconstruct array with prefix sum.

---

## Template: Range Addition

```python
def range_addition(length: int, updates: list[list[int]]) -> list[int]:
    """
    Apply multiple range additions and return final array.

    Updates format: [[start, end, value], ...]

    Time: O(n + k) where k = number of updates
    Space: O(n)

    Example:
    length = 5, updates = [[1,3,2], [2,4,3], [0,2,-2]]
    → [-2, 0, 3, 5, 3]
    """
    diff = [0] * (length + 1)  # Extra element for j+1

    # Apply all updates to difference array
    for start, end, val in updates:
        diff[start] += val
        diff[end + 1] -= val

    # Reconstruct with prefix sum
    result = [0] * length
    current = 0
    for i in range(length):
        current += diff[i]
        result[i] = current

    return result
```

### Visual Trace

```
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

```python
def car_pooling(trips: list[list[int]], capacity: int) -> bool:
    """
    Check if car can complete all trips without exceeding capacity.
    trips[i] = [numPassengers, startLocation, endLocation]

    Time: O(n + max_location)
    Space: O(max_location)

    Example:
    trips = [[2,1,5], [3,3,7]], capacity = 4 → False
    trips = [[2,1,5], [3,3,7]], capacity = 5 → True
    """
    # Find max location
    max_loc = max(trip[2] for trip in trips)

    # Difference array
    diff = [0] * (max_loc + 2)

    for passengers, start, end in trips:
        diff[start] += passengers
        diff[end] -= passengers  # Passengers get off at end

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

```python
def min_meeting_rooms(intervals: list[list[int]]) -> int:
    """
    Minimum number of meeting rooms required.

    Time: O(n + max_time)
    Space: O(max_time)

    Example:
    [[0,30], [5,10], [15,20]] → 2
    """
    if not intervals:
        return 0

    max_time = max(interval[1] for interval in intervals)
    diff = [0] * (max_time + 2)

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

```python
def min_meeting_rooms_events(intervals: list[list[int]]) -> int:
    """
    Using sorted events instead of difference array.
    Better when time range is large but intervals are few.

    Time: O(n log n) for sorting
    Space: O(n)
    """
    events = []
    for start, end in intervals:
        events.append((start, 1))   # Meeting starts
        events.append((end, -1))    # Meeting ends

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

```python
def corp_flight_bookings(bookings: list[list[int]], n: int) -> list[int]:
    """
    Each booking: [first, last, seats] books seats on flights first to last.
    Return total seats for each flight.

    Time: O(n + k)
    Space: O(n)

    Example:
    bookings = [[1,2,10], [2,3,20], [2,5,25]], n = 5
    → [10, 55, 45, 25, 25]
    """
    diff = [0] * (n + 2)

    for first, last, seats in bookings:
        diff[first] += seats
        diff[last + 1] -= seats

    result = []
    current = 0
    for i in range(1, n + 1):
        current += diff[i]
        result.append(current)

    return result
```

---

## 2D Difference Array

For 2D range updates, we need 4 operations per update:

```python
def range_addition_2d(matrix: list[list[int]],
                      updates: list[tuple]) -> list[list[int]]:
    """
    Apply 2D range additions.
    updates: [(r1, c1, r2, c2, val), ...]

    Time: O(m*n + k)
    Space: O(m*n)
    """
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
            diff[i][j] += (diff[i-1][j] if i > 0 else 0)
            diff[i][j] += (diff[i][j-1] if j > 0 else 0)
            diff[i][j] -= (diff[i-1][j-1] if i > 0 and j > 0 else 0)
            result[i][j] = matrix[i][j] + diff[i][j]

    return result
```

---

## Prefix Sum vs Difference Array

| Operation | Prefix Sum | Difference Array |
|-----------|------------|------------------|
| Build | O(n) | O(n) |
| Range Query | O(1) | O(n) |
| Range Update | O(n) | O(1) |
| Point Update | O(n) | O(1) |
| Point Query | O(1) | O(n) |

**Use Prefix Sum when**: Many queries, few/no updates
**Use Difference Array when**: Many updates, few queries

---

## Converting Between Them

```python
# Original array to difference array
def to_difference(arr: list[int]) -> list[int]:
    if not arr:
        return []
    diff = [arr[0]]
    for i in range(1, len(arr)):
        diff.append(arr[i] - arr[i-1])
    return diff

# Difference array to original array (prefix sum)
def to_original(diff: list[int]) -> list[int]:
    if not diff:
        return []
    arr = [diff[0]]
    for i in range(1, len(diff)):
        arr.append(arr[-1] + diff[i])
    return arr
```

---

## Edge Cases

```python
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

| # | Problem | Difficulty | Key Concept |
|---|---------|------------|-------------|
| 1 | Range Addition | Medium | Basic difference array |
| 2 | Car Pooling | Medium | Capacity check |
| 3 | Corporate Flight Bookings | Medium | 1-indexed bookings |
| 4 | Meeting Rooms II | Medium | Maximum concurrent |
| 5 | My Calendar III | Hard | Maximum overlapping events |
| 6 | Brightest Position on Street | Medium | Light intensity |

---

## Key Takeaways

1. **Difference array = inverse of prefix sum**
2. **Range update in O(1)**: add at start, subtract at end+1
3. **Reconstruct with prefix sum** after all updates
4. **Great for batch updates** with single reconstruction
5. **Event-based alternative** when range is sparse
6. **2D version** uses 4 operations per update

---

## Next: [08-kadanes-algorithm.md](./08-kadanes-algorithm.md)

Learn Kadane's algorithm for maximum subarray problems.
