# Gas Station

> **Prerequisites:** [Greedy Basics](./01-greedy-basics.md)

## Interview Context

Gas station tests your ability to:

1. **Circular array thinking**: Handling wrap-around logic
2. **Greedy insight**: Deriving a single-pass solution from the problem structure
3. **Proof skills**: Explaining why the greedy elimination is sound
4. **Edge case handling**: Detecting when no solution exists

---

## Problem Statement

There are `n` gas stations in a circle. You have a car with unlimited tank capacity. At station `i`:

- You gain `gas[i]` fuel
- You spend `cost[i]` fuel to travel to station `i+1`

Find the starting station index to complete the circuit, or return -1 if impossible. If a solution exists, it is **guaranteed to be unique**.

```python
Input:  gas  = [1, 2, 3, 4, 5]
        cost = [3, 4, 5, 1, 2]
Output: 3

Explanation:
# Start at station 3 (gas[3] = 4)
# Station 3: tank = 4 - 1 = 3
# Station 4: tank = 3 + 5 - 2 = 6
# Station 0: tank = 6 + 1 - 3 = 4
# Station 1: tank = 4 + 2 - 4 = 2
# Station 2: tank = 2 + 3 - 5 = 0
# Return to station 3 with tank = 0 (complete)
```

---

## Building Intuition

### The "Net Gain" Mental Model

At each station, you gain gas and spend cost to reach the next station. Think of this as a "net gain" at each stop:

```python
gas  = [1, 2, 3, 4, 5]
cost = [3, 4, 5, 1, 2]
gain = [-2, -2, -2, +3, +3]  (gas - cost)

# Sum of all gains: -2 - 2 - 2 + 3 + 3 = 0
# Total gain >= 0 means enough fuel exists -- we just need the right starting point!
```

### The "Valley and Peak" Insight

Imagine plotting cumulative fuel as you drive from station `0`:

```text
Station:     0    1    2    3    4
Gain:       -2   -2   -2   +3   +3
Cumulative: -2   -4   -6   -3    0
                        ^
                  Valley (minimum = -6)
```

The cumulative fuel hits its lowest point at station `2`. If we start right after the valley (station `3`), we accumulate fuel on the positive-gain side first, building enough buffer to survive the negative-gain side when we wrap around.

```text
Starting at station 3:
Station:     3    4    0    1    2
Gain:       +3   +3   -2   -2   -2
Tank:        3    6    4    2    0   <-- Never goes negative!
```

---

## The Two Key Insights

> **Insight 1 -- Feasibility**: If `sum(gas) >= sum(cost)`, a solution **must** exist.
>
> The total fuel available across all stations is enough to cover the total cost.
> We just need to find the right starting point so the tank never dips below zero.

> **Insight 2 -- Greedy Elimination**: If starting from station `i` causes the tank
> to go negative at station `j`, then **no station in `[i, j]` can be a valid start**.
> The next candidate is `j + 1`.
>
> This is why we solve in $O(n)$ -- when we fail, we skip _all_ intermediate stations.

### Why Failing at `j` Rules Out Stations `i` Through `j`

This is the key argument that makes the single-pass algorithm work:

```text
Suppose we start at station i and fail at station j
(i.e., the tank goes negative after processing gain[j]).
Let gain[k] = gas[k] - cost[k].

1. Because we reached j without failing earlier, the running tank was
   non-negative at every station k in [i, j-1].
   Formally: sum(gain[i..k]) >= 0 for all k in [i, j-1].

2. Because we failed at j, the total from i through j is negative:
   sum(gain[i..j]) < 0

3. Now consider starting at some station k where i < k <= j-1.
   The fuel upon reaching j would be sum(gain[k..j]).

4. We know: sum(gain[i..j]) = sum(gain[i..k-1]) + sum(gain[k..j]) < 0
   Since sum(gain[i..k-1]) >= 0 (from step 1), it follows that sum(gain[k..j]) < 0.
   So starting at k still fails at or before j.

5. What about station j itself? The tank before processing j was >= 0,
   and after adding gain[j] it went negative, so gain[j] < 0.
   Starting fresh at j gives tank = gain[j] < 0 -- immediate failure.

Conclusion: No station in [i, j] can be a valid start. Skip to j+1!
```

---

## Solution

```python
def can_complete_circuit(gas: list[int], cost: list[int]) -> int:
    """
    Find starting station to complete circular trip.

    Greedy: Track running tank. If negative, restart from next station.
    If total gas >= total cost, solution exists and will be found.

    Time:  O(n)
    Space: O(1)
    """
    total_tank = 0    # Total gain across all stations; >= 0 means a solution exists
    current_tank = 0  # Running tank from current start candidate
    start = 0         # Current candidate starting station

    for i in range(len(gas)):
        gain = gas[i] - cost[i]
        total_tank += gain
        current_tank += gain

        if current_tank < 0:
            # Can't reach station i+1 from current start.
            # By elimination, no station in [start, i] works.
            start = i + 1
            current_tank = 0

    # If total >= 0, solution exists at start
    return start if total_tank >= 0 else -1
```

### Why `start` Never Goes Out of Bounds When a Solution Exists

What if `start` keeps resetting and eventually becomes `n`?

```text
If start becomes n, it means we failed at station n-1.
This implies: sum(gain[0..n-1]) < 0 (since we accumulated all gains into total_tank).
But total_tank < 0 means NO solution exists!

So when a solution exists (total_tank >= 0), start is guaranteed to be < n.
```

This is why the algorithm needs no explicit bounds checking on `start`. (Assuming `n >= 1` as typically guaranteed).

---

## Visual Trace

### Algorithm Trace (step-by-step)

```python
# gas  = [1, 2, 3, 4, 5]
# cost = [3, 4, 5, 1, 2]
# gain = [-2, -2, -2, 3, 3]  (gas - cost)

# total_tank = -2 - 2 - 2 + 3 + 3 = 0 >= 0, so a solution exists.

# Simulation:
# i=0: gain = -2, total_tank = -2, current_tank = -2
#      current_tank < 0 -> reset: current_tank = 0, start = 1
#
# i=1: gain = -2, total_tank = -4, current_tank = -2
#      current_tank < 0 -> reset: current_tank = 0, start = 2
#
# i=2: gain = -2, total_tank = -6, current_tank = -2
#      current_tank < 0 -> reset: current_tank = 0, start = 3
#
# i=3: gain =  3, total_tank = -3, current_tank =  3
#      current_tank >= 0, continue
#
# i=4: gain =  3, total_tank =  0, current_tank =  6
#      current_tank >= 0, continue
#
# total_tank = 0 >= 0 -> return start = 3
```

### Tank Level Diagram (starting at station 3)

```text
Tank
  6 |            *
  5 |           /|
  4 |          / *
  3 |   *     /  |
  2 |   |\   /   *
  1 |   | \ /    |
  0 *---+--*     +---*
    |   |  |     |   |
    3   4  0     1   2   (station)
      +3  +3  -2  -2  -2   (gain)

Station-by-station:
  Start at 3: tank = 0 + 4 - 1 = 3
  Arrive at 4: tank = 3 + 5 - 2 = 6
  Arrive at 0: tank = 6 + 1 - 3 = 4
  Arrive at 1: tank = 4 + 2 - 4 = 2
  Arrive at 2: tank = 2 + 3 - 5 = 0  (complete!)

Tank never dips below 0 -- station 3 is valid.
```

---

## Proof of Correctness

### Part 1: If `sum(gas) >= sum(cost)`, a solution exists

Consider plotting cumulative gain starting from station `0`. The final cumulative value equals `sum(gas) - sum(cost) >= 0`. Now find the station `m` where this cumulative gain reaches its **minimum**. Starting at `(m + 1) % n`, the tank at every subsequent station (in circular order) is shifted up by `|min|`, so it never goes negative.

Formally: let `prefix[k] = sum(gain[0..k])` (inclusive). Let `m = argmin(prefix)`. Starting at `(m + 1) % n`, the tank at any station `k` (in circular order from `m + 1`) equals `prefix[k] - prefix[m]`, which is `>= 0` since `prefix[m]` is the global minimum.

### Part 2: The greedy algorithm finds it

**Claim**: If we fail at station `j` starting from `i`, no station in `[i, j]` can be the answer. The next candidate is `j+1`.

**Proof**:

Let `gain[k] = gas[k] - cost[k]` and define `sum(gain[a..b])` as the cumulative gain from station `a` to station `b` (inclusive).

1. **Premise**: Starting from `i`, we reached station `j-1` without the tank going negative,
   but after processing station `j`, the tank went negative:
   - `sum(gain[i..k]) >= 0` for all `k` in `[i, j-1]` (we didn't reset earlier)
   - `sum(gain[i..j]) < 0` (we failed at j)

2. **Stations i+1 through j-1**: Pick any station `k` where `i < k <= j-1`.
   - We can decompose: `sum(gain[i..j]) = sum(gain[i..k-1]) + sum(gain[k..j])`
   - We know `sum(gain[i..j]) < 0` (failed at j)
   - We know `sum(gain[i..k-1]) >= 0` (tank was non-negative when we passed through k-1)
   - Therefore: `sum(gain[k..j]) < 0`
   - Starting at `k` instead of `i` still fails at or before station `j`.

3. **Station j itself**:
   - Before processing station `j`, the tank was `sum(gain[i..j-1]) >= 0`
   - After adding `gain[j]`, the tank became negative: `sum(gain[i..j-1]) + gain[j] < 0`
   - This implies `gain[j] < 0` (since we're adding a negative that overcomes a non-negative)
   - Starting fresh at `j` means `tank = gain[j] < 0` -- immediate failure.

**Conclusion**: No station in `[i, j]` can be valid. We can safely skip to `j+1`.
If a solution exists (total >= 0), the final `start` position after all resets must be correct.

---

## Alternative: Minimum Tank Position

Find the position where cumulative tank reaches its minimum. Start right after it.

```python
def can_complete_circuit_v2(gas: list[int], cost: list[int]) -> int:
    """
    Alternative approach: find minimum cumulative point.

    Starting right after the minimum avoids ever going negative.

    Time:  O(n)
    Space: O(1)
    """
    total = 0
    min_tank = 0
    min_index = -1

    for i in range(len(gas)):
        total += gas[i] - cost[i]
        if total < min_tank:
            min_tank = total
            min_index = i

    if total < 0:
        return -1

    # Start from the station after the minimum point
    return (min_index + 1) % len(gas)
```

### Intuition

```text
cumulative: -2  -4  -6  -3   0

Index:       0   1   2   3   4
                     ^
               min at index 2 (value -6)

Starting at index 3 (right after the minimum):
- We hit the positive-gain stations first (+3, +3), building a fuel buffer.
- When we wrap around to the negative-gain stations (0, 1, 2),
  the accumulated buffer carries us through.
```

### Relationship Between the Two Approaches

Both approaches are fundamentally equivalent:

| Aspect              | Greedy Reset (v1)              | Minimum Cumulative (v2)        |
| ------------------- | ------------------------------ | ------------------------------ |
| **Core idea**       | Skip invalid starts            | Start after the valley         |
| **What it tracks**  | Running tank from candidate    | Global minimum cumulative      |
| **Result**          | First valid candidate          | Index after minimum + 1        |
| **Intuition**       | Elimination-based              | Geometry-based (shift up)      |

The greedy reset approach effectively finds the same answer as the minimum cumulative approach:
- When we reset at station `j`, we're saying "the cumulative minimum is at or before `j`"
- The final `start` position equals `(min_index + 1) % n` from approach 2

---

## When NOT to Use This Approach

**1. When Fuel Capacity Is Limited**

The standard problem assumes an unlimited tank. If the tank has a maximum capacity:

```text
If tank capacity is 10 and at some point we need to
hold 15 units, even a valid "start point" might fail.

This requires tracking the maximum tank level needed, not just the running total.
```

**2. When Multiple Valid Starts Are Needed**

The standard problem guarantees a unique answer. If the problem asks for all valid starting stations:

```text
gas  = [1, 1, 1]
cost = [1, 1, 1]
gain = [0, 0, 0]

Every station works! The standard algorithm returns 0,
but finding all valid starts requires a different approach.
```

**3. When Stations Can Be Skipped**

If you can skip stations (avoiding both their gas and their cost), the greedy
elimination property breaks down because the circular constraint changes:

```text
gas  = [1, 10, 1]
cost = [5, 5, 5]
gain = [-4, 5, -4]

Standard: sum(gas) = 12 < sum(cost) = 15 -> no solution.

But if we can skip station 0 (skip its gas and cost):
  Start at 1: tank = 10 - 5 = 5
  Station 2: tank = 5 + 1 - 5 = 1 (then skip back to station 1)
  We complete a partial circuit: 1 -> 2 -> 1 (valid if skipping allowed)

With skipping, the problem becomes DP or search -- the greedy
elimination property no longer holds.
```

**4. Non-circular Routes**

If the route is linear (start to end, no wrap), the problem simplifies to checking whether the tank stays non-negative throughout:

```python
def can_complete_linear(gas: list[int], cost: list[int]) -> bool:
    """
    Check if car can complete linear (non-circular) route starting from index 0.
    Simpler version without wrap-around logic.

    Time:  O(n)
    Space: O(1)
    """
    tank = 0
    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        if tank < 0:
            return False
    return True
```

---

## Variations

### 1. Minimum Starting Fuel

Find the minimum initial fuel needed to complete the circuit starting from index 0.

```python
def min_starting_fuel(gas: list[int], cost: list[int]) -> int:
    """
    Find minimum initial fuel to complete circuit from index 0.
    Track the lowest the tank ever drops; that deficit is the
    amount of fuel we'd need to bring upfront.

    Time:  O(n)
    Space: O(1)
    """
    tank = 0
    min_tank = 0

    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        min_tank = min(min_tank, tank)

    # If min_tank is -5, we need 5 units of initial fuel
    # to keep the tank non-negative at all times
    return -min_tank
```

### Brute Force Comparison

Here's the brute force approach to understand why greedy is better:

```python
def can_complete_brute_force(gas: list[int], cost: list[int]) -> int:
    """
    Brute force: try each station as starting point.
    
    Time: O(n²) - try each of n starts, each may traverse n stations
    Space: O(1) - only local variables
    """
    n = len(gas)
    
    for start in range(n):
        tank = 0
        valid = True
        
        for i in range(n):
            idx = (start + i) % n
            tank += gas[idx] - cost[idx]
            
            if tank < 0:
                valid = False
                break
        
        if valid:
            return start
    
    return -1
```

**Why greedy is better**: Instead of trying all n starting points (O(n²)), the greedy solution eliminates impossible candidates in a single pass (O(n)).

**Trace comparison for `gas = [1,2,3,4,5], cost = [3,4,5,1,2]`:**

```text
Brute Force:
- Try start=0: fails at station 2 (tank goes negative)
- Try start=1: fails at station 3
- Try start=2: fails at station 4
- Try start=3: succeeds! (4 iterations)
- Total: O(n²) = 25 operations

Greedy:
- Start at 0, tank goes negative at station 2
- Eliminate stations 0,1,2 as invalid starts
- Start at 3, succeeds in one pass
- Total: O(n) = 5 operations
```

---

## Complexity Analysis

| Operation                | Time       | Space  | Notes          |
| ------------------------ | ---------- | ------ | -------------- |
| Greedy reset             | $O(n)$     | $O(1)$ | Single pass    |
| Min cumulative approach  | $O(n)$     | $O(1)$ | Track minimum  |
| Brute force (comparison) | $O(n^{2})$ | $O(1)$ | Try each start |

---

## Edge Cases

- [ ] **Single station with gas[0] >= cost[0]**: return 0 (trivial circuit)
- [ ] **Single station with gas[0] < cost[0]**: return -1 (impossible)
- [ ] **All gas[i] == cost[i]**: Every station works since gain = 0 everywhere.
  The algorithm returns 0 because current_tank never goes negative, so start never resets.
- [ ] **sum(gas) < sum(cost)**: return -1 (physically impossible)
- [ ] **Answer is the last station (n-1)**: Algorithm handles this correctly.
  When `start = n-1`, the loop has completed, and we return `n-1` if total_tank >= 0.
  If we reset at the last element, `start` becomes `n`, but then total_tank is negative
  (since we just added a negative gain that made current_tank < 0), so we return -1 instead.
- [ ] **Multiple valid starts**: Problem guarantees unique solution, but if
  gas[i] == cost[i] for all i, every station works. Algorithm returns 0.

---

## Practice Problems

| #   | Problem                           | Difficulty | Key Insight                         |
| --- | --------------------------------- | ---------- | ----------------------------------- |
| 1   | Gas Station (LC 134)              | Medium     | Greedy reset on failure             |
| 2   | Maximum Sum Circular Subarray (LC 918) | Medium | Kadane + wrap-around trick          |
| 3   | Minimum Number of Refueling Stops (LC 871) | Hard  | Max-heap greedy                     |
| 4   | Destroying Asteroids (LC 2126)    | Medium     | Greedy accumulation / sorting       |
| 5   | Circular Array Loop (LC 457)      | Medium     | Circular traversal + cycle detection|

### Worked Problem 1: Maximum Sum Circular Subarray (LC 918)

**Problem**: Given a circular integer array `nums`, find the maximum possible sum of a non-empty subarray. The subarray may wrap around the end.

**Key insight**: A wrapping subarray's sum = total_sum - (non-wrapping minimum subarray sum). So the answer is `max(max_kadane, total - min_kadane)`. The one edge case: if all values are negative, `min_kadane` equals `total` (meaning the "wrapping subarray" would be empty), so we fall back to `max_kadane`.

```python
def max_subarray_sum_circular(nums: list[int]) -> int:
    """
    Maximum sum of a subarray in a circular array.

    Case 1: Best subarray doesn't wrap -> standard Kadane.
    Case 2: Best subarray wraps -> total_sum - min_subarray_sum.
    Answer = max(case 1, case 2), unless all elements are negative.

    Time:  O(n)
    Space: O(1)
    """
    if not nums:
        return 0

    max_sum = nums[0]       # Maximum subarray sum (Kadane)
    cur_max = 0
    min_sum = nums[0]       # Minimum subarray sum (inverted Kadane)
    cur_min = 0
    total = 0

    for x in nums:
        # Standard Kadane's for max subarray
        cur_max = max(cur_max + x, x)
        max_sum = max(max_sum, cur_max)

        # Inverted Kadane's for min subarray
        cur_min = min(cur_min + x, x)
        min_sum = min(min_sum, cur_min)

        total += x

    # If all numbers are negative, total == min_sum, and max_sum will be the
    # maximum (least negative) single element. We must return max_sum to
    # avoid returning an empty subarray sum of 0 (which total - min_sum would give).
    if max_sum < 0:
        return max_sum

    return max(max_sum, total - min_sum)
```

**Trace** (`nums = [5, -3, 5]`):

```text
Initialize: max_sum=5, cur_max=0, min_sum=5, cur_min=0, total=0

i=0: x=5   cur_max=5  max_sum=5   cur_min=5  min_sum=5   total=5
i=1: x=-3  cur_max=2  max_sum=5   cur_min=-3 min_sum=-3  total=2
i=2: x=5   cur_max=7  max_sum=7   cur_min=2  min_sum=-3  total=7

Non-wrapping max = 7, wrapping max = total - min_sum = 7 - (-3) = 10
Answer = max(7, 10) = 10  (subarray [5, _, 5] wrapping around)
```

### Worked Problem 2: Minimum Number of Refueling Stops (LC 871)

**Problem**: A car starts with `startFuel` liters of fuel. It drives from position 0 to position `target` along a road. Along the way there are gas stations: `stations[i] = [position_i, fuel_i]`. The car uses 1 liter per mile. Return the minimum number of refueling stops to reach the target, or -1 if impossible.

**Key insight**: Greedily delay refueling. As we pass stations, add their fuel to a max-heap. Whenever we run out of fuel, pop the largest available refuel. This minimizes stops because each stop we "use" gives us the maximum possible fuel.

```python
def min_refuel_stops(target: int, start_fuel: int, stations: list[list[int]]) -> int:
    """
    Minimum refueling stops to reach target.

    Greedy: pass stations and record fuel in a max-heap.
    When tank runs dry, "retroactively" stop at the best station.

    Time:  O(n log n) -- each station pushed/popped from heap at most once
    Space: O(n)       -- heap stores at most n stations
    """
    import heapq

    fuel = start_fuel
    stops = 0
    heap = []  # max-heap (negate values since Python has min-heap)
    i = 0
    n = len(stations)

    while fuel < target:
        # Add all stations we can reach with current fuel
        while i < n and stations[i][0] <= fuel:
            # Push negative for max-heap behavior
            heapq.heappush(heap, -stations[i][1])
            i += 1

        if fuel >= target:
            break

        if not heap:
            return -1  # Can't reach target or any more stations

        # "Stop" at the station with the most fuel we've passed
        fuel += -heapq.heappop(heap)
        stops += 1

    return stops
```

**Trace** (`target=100, startFuel=10, stations=[[10,60],[20,30],[30,30],[60,40]]`):

```text
fuel=10: pass station [10,60] -> heap=[-60]
         pass station [20,30]? 20 > 10, stop adding
         fuel < 100, pop -60: fuel = 10+60 = 70, stops = 1

fuel=70: pass station [20,30] -> heap=[-30]
         pass station [30,30] -> heap=[-30,-30]
         pass station [60,40] -> heap=[-40,-30,-30]
         fuel < 100, pop -40: fuel = 70+40 = 110, stops = 2

fuel=110 >= 100: done! Answer = 2
```

---

### Worked Problem 3: Destroying Asteroids (LC 2126)

**Problem**: You are given an integer `mass`, which represents the original mass of a planet. You are further given an integer array `asteroids`. You can arrange for the planet to collide with the asteroids in any arbitrary order. If the mass of the planet is greater than or equal to the mass of the asteroid, the asteroid is destroyed and the planet gains the mass of the asteroid. Otherwise, the planet is destroyed. Return `true` if all asteroids can be destroyed. Otherwise, return `false`.

**Key insight**: This is a classic greedy accumulation problem. To maximize our chances of destroying all asteroids, we should always tackle the smallest asteroids first to build up our mass. If we can't destroy the smallest available asteroid, we certainly can't destroy any larger ones.

```python
def asteroids_destroyed(mass: int, asteroids: list[int]) -> bool:
    """
    Determine if planet can destroy all asteroids.

    Greedy: Sort asteroids and consume smallest first to build mass.

    Time:  O(n log n) - sorting dominates
    Space: O(1)       - ignoring sort space
    """
    # Sort to greedily consume smallest asteroids first
    asteroids.sort()

    current_mass = mass

    for asteroid in asteroids:
        if current_mass >= asteroid:
            current_mass += asteroid
        else:
            return False

    return True
```

**Trace** (`mass = 10, asteroids = [3, 9, 19, 5, 21]`):

```text
Sort asteroids: [3, 5, 9, 19, 21]

mass=10: asteroid=3  -> 10 >= 3  -> mass = 10 + 3 = 13
mass=13: asteroid=5  -> 13 >= 5  -> mass = 13 + 5 = 18
mass=18: asteroid=9  -> 18 >= 9  -> mass = 18 + 9 = 27
mass=27: asteroid=19 -> 27 >= 19 -> mass = 27 + 19 = 46
mass=46: asteroid=21 -> 46 >= 21 -> mass = 46 + 21 = 67

All destroyed! Return True.
```

---

## Interview Tips

1. **State the two observations**: total sum feasibility check + greedy reset on failure
2. **Prove elimination works**: failing at j rules out every station from i through j
3. **Trace an example**: show the reset happening in the simulation
4. **Handle no solution**: check total_tank at the end
5. **Mention uniqueness**: the problem guarantees at most one valid start

---

## Key Takeaways

1. **Feasibility**: if `sum(gas) >= sum(cost)`, a solution exists
2. **Elimination**: failing at station j eliminates every station from i through j
3. Single-pass $O(n)$ solution by tracking reset points
4. Alternative: start after the cumulative minimum point
5. The problem guarantees the solution is unique (if it exists)

---

## Next: [07-candy-distribution.md](./07-candy-distribution.md)

Learn the two-pass greedy pattern with the candy distribution problem.
