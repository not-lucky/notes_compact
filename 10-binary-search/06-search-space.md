# Binary Search on Answer Space

> **Prerequisites:** [Binary Search Template](./01-binary-search-template.md)

## Interview Context

"Binary search on answer" is a powerful pattern for optimization problems:

1. **Hidden binary search**: Not obvious that binary search applies
2. **FANG+ favorite**: Commonly asked at top companies
3. **Feasibility checking**: Transform optimization into decision problem
4. **Range of answers**: Search the possible answer values

---

## Building Intuition

**The Paradigm Shift**

Normally, binary search finds an element IN an array. But here's the twist: you can binary search on the **answer itself**.

```
Traditional Binary Search:
- Given: sorted array [1, 3, 5, 7, 9]
- Question: "Where is 5?"
- Search: in the array indices

Binary Search on Answer:
- Given: some problem constraints
- Question: "What's the minimum X that satisfies constraints?"
- Search: in the range of possible answers
```

**The Key Insight: Optimization → Decision**

Every optimization problem ("Find minimum X such that...") can be converted to a decision problem ("Can we achieve X?"):

```
Optimization: "What's the minimum speed to finish in 8 hours?"
↓ Transform to ↓
Decision: "Can we finish in 8 hours at speed 5?" → Yes/No
Decision: "Can we finish in 8 hours at speed 3?" → Yes/No
Decision: "Can we finish in 8 hours at speed 4?" → Yes/No
```

If we can answer the decision question quickly, we can binary search on the answer!

**The Monotonic Property of Feasibility**

This is WHY binary search works:

```
Speed:      [1] [2] [3] [4] [5] [6] [7] [8]
Can finish: [N] [N] [N] [Y] [Y] [Y] [Y] [Y]
                        ↑
                 First "Yes" = minimum speed

If you CAN finish at speed 4, you CAN finish at speed 5, 6, 7...
(More speed = easier to meet deadline)

This monotonic property lets us binary search!
```

**Mental Model: The Goldilocks Zone**

Imagine adjusting a dial (the answer):

- Too low: constraints not satisfied
- Too high: works, but not optimal
- Just right: the minimum value that works

Binary search finds "just right" efficiently.

**The Template Pattern**

```
1. Define the answer range: [min_possible, max_possible]
2. Write a feasibility check: is_feasible(answer) → bool
3. Verify monotonicity: is_feasible(X) implies is_feasible(X+1) (or vice versa)
4. Binary search to find the boundary
```

**Example Walkthrough: Koko's Bananas**

Problem: Eat all banana piles in H hours. Minimum eating speed?

```
Piles: [3, 6, 7, 11], H = 8 hours

Answer range: [1, 11] (min: 1 banana/hr, max: largest pile/hr)

is_feasible(speed):
  hours = ceil(3/speed) + ceil(6/speed) + ceil(7/speed) + ceil(11/speed)
  return hours <= 8

is_feasible(4)?
  hours = 1 + 2 + 2 + 3 = 8 ≤ 8 ✓

is_feasible(3)?
  hours = 1 + 2 + 3 + 4 = 10 > 8 ✗

Binary search finds: minimum speed = 4
```

---

## When NOT to Use Binary Search on Answer

**1. Non-Monotonic Feasibility**

If "works at X" doesn't imply "works at X+1", binary search fails:

```
Bad Example: "Find X where X² = 16"
is_feasible(3) = 9 ≠ 16 → No
is_feasible(4) = 16 = 16 → Yes
is_feasible(5) = 25 ≠ 16 → No

Not monotonic! Binary search won't work.
(Though this specific example has better solutions anyway)
```

**2. Discrete Answers with Gaps**

If valid answers aren't contiguous, binary search may miss them:

```
Valid answers: {1, 5, 10, 15}  (not all integers in range)
Binary search assumes continuous search space.
```

**3. Expensive Feasibility Check**

If `is_feasible(X)` takes O(n²) time:

- Total time = O(log(range) × n²)
- Might be worse than brute force O(n × range)

**4. Small Answer Range**

If range is only 10-20 values:

- Linear scan is O(range)
- Binary search is O(log(range)) — marginal improvement
- Linear scan is simpler to implement

**Red Flags:**

- "Find exact value X where..." → May not be monotonic
- "Which of these specific options..." → Discrete choices, not range
- "Minimize function with multiple local minima" → Ternary search or calculus

---

## The Pattern

Instead of searching in an array, search in the **range of possible answers**:

```
Problem: Find minimum X such that condition(X) is true

Answer range: [min_possible, max_possible]
Search: Binary search on this range
Check: Is condition(mid) feasible?
```

The key insight: **if condition is true for X, it's true for all X' > X** (or vice versa).

---

## Template: Binary Search on Answer

```python
def binary_search_answer(low: int, high: int, is_feasible) -> int:
    """
    Find minimum value where is_feasible returns True.

    is_feasible: function that returns True if answer is feasible

    Time: O(log(high-low) * cost_of_is_feasible)
    Space: O(1)
    """
    result = high  # or -1 if no feasible answer

    while low <= high:
        mid = low + (high - low) // 2

        if is_feasible(mid):
            result = mid       # Found feasible, try smaller
            high = mid - 1
        else:
            low = mid + 1      # Not feasible, need larger

    return result
```

---

## Classic Example: Koko Eating Bananas

LeetCode 875: Koko Eating Bananas

**Problem**: Koko can eat `k` bananas per hour. Given piles and `h` hours, find minimum `k` to eat all bananas.

```python
def min_eating_speed(piles: list[int], h: int) -> int:
    """
    Find minimum eating speed to finish all piles in h hours.

    Time: O(n * log(max(piles)))
    Space: O(1)
    """
    def can_finish(k: int) -> bool:
        """Check if Koko can finish with speed k."""
        hours = 0
        for pile in piles:
            hours += (pile + k - 1) // k  # Ceiling division
        return hours <= h

    # Answer range: [1, max(piles)]
    left, right = 1, max(piles)

    while left < right:
        mid = left + (right - left) // 2

        if can_finish(mid):
            right = mid        # Can finish, try slower
        else:
            left = mid + 1     # Can't finish, need faster

    return left
```

**Why this works:**

- If Koko can finish with speed `k`, she can finish with any speed `> k`
- Monotonic property: [False, False, ..., True, True, True]
- Binary search finds the first True

---

## Capacity to Ship Packages

LeetCode 1011: Capacity To Ship Packages Within D Days

```python
def ship_within_days(weights: list[int], days: int) -> int:
    """
    Find minimum ship capacity to ship all packages in D days.

    Time: O(n * log(sum(weights)))
    Space: O(1)
    """
    def can_ship(capacity: int) -> bool:
        """Check if we can ship all packages with given capacity."""
        days_needed = 1
        current_load = 0

        for weight in weights:
            if current_load + weight > capacity:
                days_needed += 1
                current_load = weight
            else:
                current_load += weight

        return days_needed <= days

    # Minimum capacity: max weight (must fit largest package)
    # Maximum capacity: sum of all weights (ship everything at once)
    left = max(weights)
    right = sum(weights)

    while left < right:
        mid = left + (right - left) // 2

        if can_ship(mid):
            right = mid
        else:
            left = mid + 1

    return left
```

---

## Split Array Largest Sum

LeetCode 410: Split Array Largest Sum

```python
def split_array(nums: list[int], k: int) -> int:
    """
    Split array into k subarrays to minimize the largest sum.

    Time: O(n * log(sum(nums)))
    Space: O(1)
    """
    def can_split(max_sum: int) -> bool:
        """Check if we can split with largest sum <= max_sum."""
        subarrays = 1
        current_sum = 0

        for num in nums:
            if current_sum + num > max_sum:
                subarrays += 1
                current_sum = num
            else:
                current_sum += num

        return subarrays <= k

    left = max(nums)    # At least the largest element
    right = sum(nums)   # At most the entire sum

    while left < right:
        mid = left + (right - left) // 2

        if can_split(mid):
            right = mid    # Can split, try smaller max sum
        else:
            left = mid + 1 # Can't split, need larger max sum

    return left
```

---

## Minimize Max Distance to Gas Station

LeetCode 774: Minimize Max Distance to Gas Station

```python
def minmax_gas_dist(stations: list[int], k: int) -> float:
    """
    Add k gas stations to minimize the maximum distance between stations.

    Time: O(n * log((max_dist) / precision))
    Space: O(1)
    """
    def stations_needed(max_dist: float) -> int:
        """Count stations needed to achieve max_dist."""
        count = 0
        for i in range(len(stations) - 1):
            gap = stations[i + 1] - stations[i]
            count += int(gap / max_dist)  # Stations to add in this gap
        return count

    left = 0
    right = stations[-1] - stations[0]
    precision = 1e-6

    while right - left > precision:
        mid = (left + right) / 2

        if stations_needed(mid) <= k:
            right = mid   # Can achieve, try smaller
        else:
            left = mid    # Need more stations, try larger

    return left
```

---

## Magnetic Force Between Balls

LeetCode 1552: Magnetic Force Between Two Balls

```python
def max_distance(position: list[int], m: int) -> int:
    """
    Place m balls to maximize minimum distance between any two balls.

    Time: O(n log n + n * log(max_pos - min_pos))
    Space: O(1)
    """
    position.sort()

    def can_place(min_dist: int) -> bool:
        """Check if we can place m balls with at least min_dist apart."""
        balls = 1
        last_pos = position[0]

        for i in range(1, len(position)):
            if position[i] - last_pos >= min_dist:
                balls += 1
                last_pos = position[i]
                if balls == m:
                    return True

        return False

    left = 1
    right = position[-1] - position[0]

    while left < right:
        mid = left + (right - left + 1) // 2  # Upper mid for max search

        if can_place(mid):
            left = mid      # Can place, try larger distance
        else:
            right = mid - 1 # Can't place, try smaller

    return left
```

**Note**: When maximizing, use `left = mid` and upper mid (`(right - left + 1) // 2`).

---

## Finding the Pattern

### Signs that binary search on answer applies:

1. **"Minimum/maximum X such that..."**
2. **Optimization with constraint**
3. **Feasibility function is monotonic**
4. **Answer range is bounded and searchable**

### Questions to ask yourself:

1. What is the answer range? `[min_possible, max_possible]`
2. Can I check if a specific answer is feasible?
3. Is feasibility monotonic? (If true for X, what about X+1?)

---

## Minimizing vs Maximizing

### Minimizing (find smallest feasible):

```python
# Looking for: [False, False, True, True, True]
#                             ↑ find this

while left < right:
    mid = left + (right - left) // 2
    if is_feasible(mid):
        right = mid        # Feasible, try smaller
    else:
        left = mid + 1     # Not feasible, need larger
```

### Maximizing (find largest feasible):

```python
# Looking for: [True, True, True, False, False]
#                         ↑ find this

while left < right:
    mid = left + (right - left + 1) // 2  # Upper mid!
    if is_feasible(mid):
        left = mid         # Feasible, try larger
    else:
        right = mid - 1    # Not feasible, need smaller
```

---

## Complexity Analysis

| Problem       | Binary Search Range | Feasibility Check | Total Time    |
| ------------- | ------------------- | ----------------- | ------------- |
| Koko Bananas  | O(log M)            | O(n)              | O(n log M)    |
| Ship Packages | O(log S)            | O(n)              | O(n log S)    |
| Split Array   | O(log S)            | O(n)              | O(n log S)    |
| Gas Stations  | O(log D / ε)        | O(n)              | O(n log(D/ε)) |

Where M = max element, S = sum of elements, D = distance range, ε = precision.

---

## Common Mistakes

### 1. Wrong Answer Range

```python
# Wrong: starting from 0 for Koko
left = 0  # Can't eat 0 bananas per hour!

# Correct: start from 1
left = 1
```

### 2. Wrong Mid Calculation for Maximizing

```python
# Wrong: using lower mid when maximizing
mid = left + (right - left) // 2
if feasible:
    left = mid  # Infinite loop when left + 1 == right!

# Correct: use upper mid
mid = left + (right - left + 1) // 2
```

### 3. Feasibility Function Wrong Monotonicity

```python
# Make sure: if can_do(X) is True, then can_do(X+1) is also True (for minimizing)
# Or vice versa for maximizing
```

---

## Edge Cases Checklist

- [ ] Minimum possible answer
- [ ] Maximum possible answer
- [ ] Answer is at boundary
- [ ] Precision for floating-point answers
- [ ] Empty input / single element

---

## Practice Problems

| #   | Problem                                 | Difficulty | Key Insight              |
| --- | --------------------------------------- | ---------- | ------------------------ |
| 1   | Koko Eating Bananas                     | Medium     | Min speed feasibility    |
| 2   | Capacity To Ship Packages               | Medium     | Min capacity feasibility |
| 3   | Split Array Largest Sum                 | Hard       | Min max-sum feasibility  |
| 4   | Minimize Max Distance to Gas Station    | Hard       | Float binary search      |
| 5   | Magnetic Force Between Two Balls        | Medium     | Max min-distance         |
| 6   | Find the Smallest Divisor               | Medium     | Min divisor feasibility  |
| 7   | Minimum Time to Complete Trips          | Medium     | Min time feasibility     |
| 8   | Maximum Candies Allocated to K Children | Medium     | Max candies per child    |

---

## Interview Tips

1. **Identify the pattern**: "Find min/max X such that..."
2. **Define the range**: What are min and max possible answers?
3. **Write feasibility check first**: Get this right before binary search
4. **Test monotonicity**: Verify your check is monotonic
5. **Handle precision**: Use epsilon for floating-point

---

## Key Takeaways

1. **Search on answer range**: Not just arrays
2. **Monotonic feasibility**: Key requirement
3. **Transform optimization to decision**: "Can we do X?" vs "What's minimum?"
4. **Different mid for min vs max**: Avoid infinite loops
5. **Time = O(log range × feasibility cost)**: Know your complexity

---

## Next: [07-matrix-search.md](./07-matrix-search.md)

Binary search patterns for 2D matrices.
