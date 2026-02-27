# Binary Search on Answer Space

> **Prerequisites:** [Binary Search Template](./01-binary-search-template.md)

## Interview Context

"Binary search on answer" is a powerful pattern for optimization problems. It's heavily favored in FANG interviews because it requires a conceptual leap from searching data to searching the domain of possible answers.

1. **Hidden binary search**: It's often not obvious that binary search applies.
2. **Feasibility checking**: Transforms an optimization problem into a decision problem.
3. **Range of answers**: You search the continuous range of possible answer values, rather than an array of elements.

---

## Building Intuition

### The Paradigm Shift

Normally, binary search finds an element IN an array. But here's the twist: you can binary search on the **answer itself**.

```
Traditional Binary Search:
- Given: Sorted array [1, 3, 5, 7, 9]
- Question: "Where is 5?"
- Search Space: The array indices

Binary Search on Answer:
- Given: Problem constraints and a goal
- Question: "What's the minimum/maximum X that satisfies constraints?"
- Search Space: The range of possible answers [min_X, max_X]
```

### The Key Insight: Optimization → Decision

Every optimization problem ("Find minimum X such that...") can be converted to a decision problem ("Can we achieve X?"):

```
Optimization: "What's the minimum speed to finish in 8 hours?"
↓ Transform to ↓
Decision: "Can we finish in 8 hours at speed 3?" → False
Decision: "Can we finish in 8 hours at speed 4?" → True
Decision: "Can we finish in 8 hours at speed 5?" → True
```

If we can answer the decision question (the **feasibility check**) relatively quickly, we can binary search the answer range.

### The Monotonic Property of Feasibility

This is WHY binary search works here. The feasibility function must be **monotonic**:

```
Speed:      [1] [2] [3] [4] [5] [6] [7] [8]
Can finish: [F] [F] [F] [T] [T] [T] [T] [T]
                        ↑
                 First "True" = minimum valid speed
```

If you CAN finish at speed 4, you obviously CAN finish at speed 5, 6, 7...
(More speed = easier to meet the deadline).

This monotonic boolean array `[F, F, F, T, T, T]` allows us to use binary search to find the boundary.

---

## When NOT to Use Binary Search on Answer

**1. Non-Monotonic Feasibility**
If "works at X" doesn't guarantee "works at X+1", binary search fails:
- E.g., `is_feasible(3) -> False`, `is_feasible(4) -> True`, `is_feasible(5) -> False`.
- Binary search relies on discarding half the search space. Without monotonicity, you can't confidently discard a half.

**2. Expensive Feasibility Check**
If `is_feasible(X)` takes $O(N^2)$ time:
- Total time = $O(\log(\text{range}) \cdot N^2)$.
- Depending on the constraints, this might be worse than a smart $O(N \cdot \text{range})$ algorithm.

**3. Small Answer Range**
If the range is only 10-20 values:
- Linear scan is $O(\text{range})$.
- Binary search is $O(\log(\text{range}))$—the improvement is marginal, and linear scan has less overhead.

**Red Flags:**
- "Find exact value X where..." → May not be monotonic.
- "Minimize function with multiple local minima" → Requires ternary search or calculus, not binary search.

---

## The Core Patterns

There are two primary variations: finding the **minimum** feasible value and finding the **maximum** feasible value.

### 1. Minimizing (Find smallest feasible value)

Looking for the first `True` in `[F, F, F, T, T, T]`. This maps to **Template 2** (find left boundary).

```python
def minimize_answer(left: int, right: int) -> int:
    while left < right:
        # Prevent integer overflow
        mid = left + (right - left) // 2

        if is_feasible(mid):
            right = mid        # Feasible. Try to find a SMALLER feasible value.
        else:
            left = mid + 1     # Not feasible. We MUST increase the value.

    # After the loop, left == right, which is the minimum feasible value
    # as long as a valid answer exists in the initial [left, right] range.
    # Otherwise, you might need an additional check: return left if is_feasible(left) else -1
    return left
```

### 2. Maximizing (Find largest feasible value)

Looking for the last `True` in `[T, T, T, F, F, F]`. This maps to **Template 3** (find right boundary).

```python
def maximize_answer(left: int, right: int) -> int:
    while left < right:
        # IMPORTANT: Use upper mid to avoid infinite loops when right = left + 1
        # E.g., if left=4, right=5. If we used standard mid, mid=4.
        # If is_feasible(4) is True, left = mid = 4. Infinite loop!
        mid = left + (right - left + 1) // 2

        if is_feasible(mid):
            left = mid         # Feasible. Try to find a LARGER feasible value.
        else:
            right = mid - 1    # Not feasible. We MUST decrease the value.

    # After the loop, left == right, which is the maximum feasible value
    # assuming a valid answer exists.
    # Note: If no valid answer exists, it might return left, so check is_feasible(left)
    return left
```

---

## Classic Examples

### 1. Koko Eating Bananas (Minimization)

LeetCode 875: Koko Eating Bananas
**Problem**: Koko can eat `k` bananas per hour. Given piles and `h` hours, find the **minimum** `k` to eat all bananas.

```python
def min_eating_speed(piles: list[int], h: int) -> int:
    """
    Time: O(N log(max(piles))) where N is len(piles)
    Space: O(1)
    """
    def can_finish(speed: int) -> bool:
        hours = 0
        for pile in piles:
            # Equivalent to math.ceil(pile / speed) but uses integer math
            hours += (pile + speed - 1) // speed
        return hours <= h

    # Answer range: [1, max(piles)]
    # Min speed is 1 (can't eat 0/hr). Max speed needed is max(piles) because
    # eating faster than the largest pile doesn't save any more time.
    left, right = 1, max(piles)

    while left < right:
        # Prevent integer overflow
        mid = left + (right - left) // 2

        if can_finish(mid):
            right = mid        # Try smaller speed
        else:
            left = mid + 1     # Speed too slow, must increase

    return left
```

### 2. Capacity to Ship Packages (Minimization)

LeetCode 1011: Capacity To Ship Packages Within D Days
**Problem**: Find the **minimum** ship capacity to ship all packages in `D` days in order.

```python
def ship_within_days(weights: list[int], days: int) -> int:
    """
    Time: O(N log(sum(weights) - max(weights)))
    Space: O(1)
    """
    def can_ship(capacity: int) -> bool:
        days_needed = 1
        current_load = 0

        for weight in weights:
            if current_load + weight > capacity:
                days_needed += 1
                current_load = weight
            else:
                current_load += weight

        return days_needed <= days

    # Minimum capacity MUST be at least the heaviest package (otherwise it can never ship)
    # Maximum capacity is sum of all weights (ship everything in 1 day)
    left, right = max(weights), sum(weights)

    while left < right:
        # Prevent integer overflow
        mid = left + (right - left) // 2

        if can_ship(mid):
            right = mid        # Capacity is sufficient, try smaller
        else:
            left = mid + 1     # Capacity is too small, must increase

    return left
```

### 3. Magnetic Force Between Two Balls (Maximization)

LeetCode 1552: Magnetic Force Between Two Balls
**Problem**: Place `m` balls in given `position` baskets to **maximize** the minimum distance between any two balls.

```python
def max_distance(position: list[int], m: int) -> int:
    """
    Time: O(N log N + N log(max_pos - min_pos))
    Space: O(N) for sorting (Timsort in Python)
    """
    position.sort()

    def can_place(min_dist: int) -> bool:
        balls_placed = 1
        last_pos = position[0]

        for i in range(1, len(position)):
            if position[i] - last_pos >= min_dist:
                balls_placed += 1
                last_pos = position[i]
                if balls_placed == m:
                    return True

        return False

    # Min possible distance is 1
    # Max possible distance is placing balls at the absolute extremes
    left, right = 1, position[-1] - position[0]

    while left < right:
        # Maximizing, so use UPPER mid!
        # mid = left + (right - left + 1) // 2 prevents infinite loops
        mid = left + (right - left + 1) // 2

        if can_place(mid):
            left = mid         # Valid. Try to find an even LARGER distance
        else:
            right = mid - 1    # Invalid. Must decrease distance

    return left
```

### 4. Floating Point Search: Max Distance to Gas Station

LeetCode 774: Minimize Max Distance to Gas Station (Premium)
**Problem**: Add `k` gas stations to minimize the maximum distance between adjacent stations.

**FANG Pro-Tip for Floating Point Binary Search**:
Instead of relying on a `while right - left > epsilon:` loop, which can cause infinite loops due to floating point precision errors, **run the loop a fixed number of times** (e.g., 60-100 times). Since $2^{60}$ provides massive precision, this guarantees precision without infinite loop risks.

```python
def minmax_gas_dist(stations: list[int], k: int) -> float:
    """
    Time: O(N * 60) -> O(N)
    Space: O(1)
    """
    def stations_needed(max_dist: float) -> int:
        count = 0
        for i in range(len(stations) - 1):
            gap = stations[i + 1] - stations[i]
            # How many stations to add in this gap to ensure no distance > max_dist
            count += int(gap / max_dist)
        return count

    left = 0.0
    right = float(stations[-1] - stations[0])

    # Run exactly 60 iterations for floating point precision.
    # 2^60 is ~10^18, providing extreme precision safely.
    for _ in range(60):
        mid = left + (right - left) / 2.0

        if stations_needed(mid) <= k:
            right = mid   # Can achieve this distance with k or fewer stations. Try smaller.
        else:
            left = mid    # Need more than k stations. Must allow larger distance.

    # After 60 iterations, left and right are practically equal.
    # We want the minimum max_dist, which is where they converge.
    return left
```

---

## Complexity Analysis

| Problem | Search Range | Feasibility Check | Total Time | Space |
| :--- | :--- | :--- | :--- | :--- |
| **Koko Bananas** | $O(\log M)$ | $O(N)$ | $O(N \log M)$ | $O(1)$ |
| **Ship Packages** | $O(\log S)$ | $O(N)$ | $O(N \log S)$ | $O(1)$ |
| **Split Array** | $O(\log S)$ | $O(N)$ | $O(N \log S)$ | $O(1)$ |
| **Mag Force** | $O(\log D)$ | $O(N)$ | $O(N \log N + N \log D)$* | $O(N)$ |

*\*Where $M$ = max element, $S$ = sum of elements, $D$ = distance range, $N$ = size of array.*
*\*Magnetic force requires initial sorting: $O(N \log N)$ time, $O(N)$ space in Python (Timsort) or $O(\log N)$ in C++ (`std::sort`) / Java (`Arrays.sort`).*

---

## Common Mistakes & How to Avoid Them

### 1. Infinite Loops when Maximizing
**Mistake**: Using `mid = left + (right - left) // 2` when looking for the maximum valid answer.
**Why**: If `left = 4` and `right = 5`, `mid = 4`. If `is_feasible(4)` is True, we set `left = mid` (so `left = 4`). The loop repeats forever.
**Fix**: Use upper mid: `mid = left + (right - left + 1) // 2`. Now `mid = 5`. If `is_feasible(5)` is False, `right = mid - 1` (so `right = 4`), loop terminates.

### 2. Setting Incorrect Answer Range Boundaries
**Mistake**: Automatically starting `left = 0` or `left = 1` for everything.
**Fix**: Think critically about the domain. In the "Ship Packages" problem, a ship's capacity **cannot be less than the heaviest package**, otherwise that single package can never ship. `left = max(weights)`. On the other hand, the maximum capacity `right = sum(weights)` (shipping everything in 1 day). Shrinking boundaries tightly makes the code more robust and potentially slightly faster.

### 3. Floating Point Precision Infinite Loops
**Mistake**: `while right - left > 1e-6:` can infinite loop if float representation cannot accurately represent the gap.
**Fix**: Use the fixed-iteration loop pattern (`for _ in range(60):`) for floating point binary search.

---

## Practice Problems

| # | Problem | Difficulty | Key Insight |
| :--- | :--- | :---: | :--- |
| 875 | [Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/) | Medium | Min speed feasibility |
| 1011| [Capacity To Ship Packages Within D Days](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/) | Medium | Min capacity feasibility |
| 410 | [Split Array Largest Sum](https://leetcode.com/problems/split-array-largest-sum/) | Hard | Min max-sum feasibility |
| 774 | [Minimize Max Distance to Gas Station](https://leetcode.com/problems/minimize-max-distance-to-gas-station/) | Hard | Float binary search |
| 1552| [Magnetic Force Between Two Balls](https://leetcode.com/problems/magnetic-force-between-two-balls/) | Medium | Max min-distance |
| 1283| [Find the Smallest Divisor Given a Threshold](https://leetcode.com/problems/find-the-smallest-divisor-given-a-threshold/) | Medium | Min divisor feasibility |
| 2187| [Minimum Time to Complete Trips](https://leetcode.com/problems/minimum-time-to-complete-trips/) | Medium | Min time feasibility |

---

## Interview Tips

1. **Identify the pattern**: Look for "Find min/max X such that..." or optimization with a constraint.
2. **Abstract the Feasibility**: Write the `is_feasible()` function signature early. Let your brain treat it as a black box while you write the binary search template.
3. **Determine Monotonicity**: Clearly state to the interviewer: "Because if we can finish at speed $X$, we can definitively finish at speed $X+1$, the search space is monotonic and we can binary search."
4. **Determine Boundaries**: Clearly justify your `left` and `right` initial values.

---

## Next: [07-matrix-search.md](./07-matrix-search.md)

Binary search patterns for 2D matrices.
