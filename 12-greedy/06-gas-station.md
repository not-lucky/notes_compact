# Gas Station

> **Prerequisites:** [Greedy Basics](./01-greedy-basics.md)

## Interview Context

Gas station tests:
1. **Circular array thinking**: Handling wrap-around
2. **Greedy insight**: Single-pass solution
3. **Proof skills**: Why the greedy approach works
4. **Edge case handling**: No solution exists

---

## Problem Statement

There are `n` gas stations in a circle. You have a car with unlimited tank capacity. At station `i`:
- You gain `gas[i]` fuel
- You spend `cost[i]` fuel to travel to station `i+1`

Find the starting station index to complete the circuit, or return -1 if impossible.

```
Input:  gas  = [1, 2, 3, 4, 5]
        cost = [3, 4, 5, 1, 2]
Output: 3

Explanation:
Start at station 3 (gas[3] = 4)
Station 3: tank = 4 - 1 = 3
Station 4: tank = 3 + 5 - 2 = 6
Station 0: tank = 6 + 1 - 3 = 4
Station 1: tank = 4 + 2 - 4 = 2
Station 2: tank = 2 + 3 - 5 = 0
Return to station 3 with tank = 0 ✓
```

---

## The Core Insight

Two key observations:

1. **Feasibility check**: If `sum(gas) >= sum(cost)`, a solution exists.
2. **Greedy choice**: If starting from `i` fails at `j`, no station in `[i, j-1]` can be a valid start.

```
Why observation 2?

If we fail at station j starting from i:
- We had non-negative tank from i to j-1
- Tank went negative at j
- Starting from any k in [i+1, j-1]:
  - We'd have LESS fuel at k (missed gas[i] to gas[k-1])
  - We'd still fail at or before j

Therefore, next candidate is j+1.
```

---

## Solution

```python
def can_complete_circuit(gas: list[int], cost: list[int]) -> int:
    """
    Find starting station to complete circular trip.

    Greedy: Track running tank. If negative, restart from next station.
    If total gas >= total cost, solution exists and will be found.

    Time: O(n)
    Space: O(1)
    """
    n = len(gas)
    total_tank = 0    # Overall feasibility
    current_tank = 0  # Current attempt
    start = 0

    for i in range(n):
        gain = gas[i] - cost[i]
        total_tank += gain
        current_tank += gain

        if current_tank < 0:
            # Can't reach i+1 from start
            # Try starting from i+1
            start = i + 1
            current_tank = 0

    # If total >= 0, solution exists at start
    return start if total_tank >= 0 else -1
```

---

## Visual Trace

```
gas  = [1, 2, 3, 4, 5]
cost = [3, 4, 5, 1, 2]
gain = [-2, -2, -2, 3, 3]  (gas - cost)

total_tank = -2 + (-2) + (-2) + 3 + 3 = 0 ≥ 0 → solution exists

Simulation:
i=0: gain=-2, current=-2 < 0 → reset, start=1
i=1: gain=-2, current=-2 < 0 → reset, start=2
i=2: gain=-2, current=-2 < 0 → reset, start=3
i=3: gain=3, current=3 ≥ 0 → continue
i=4: gain=3, current=6 ≥ 0 → continue

total_tank=0 ≥ 0, return start=3

Verify starting at 3:
3 → 4: tank = 0 + 4 - 1 = 3
4 → 0: tank = 3 + 5 - 2 = 6
0 → 1: tank = 6 + 1 - 3 = 4
1 → 2: tank = 4 + 2 - 4 = 2
2 → 3: tank = 2 + 3 - 5 = 0 ✓
```

---

## Proof of Correctness

### Part 1: If sum(gas) >= sum(cost), solution exists

**By contradiction**:
- Assume no valid starting point exists
- For every station `i`, starting there leads to negative tank somewhere
- But if we sum all journeys, total gain = sum(gas) - sum(cost) ≥ 0
- Contradiction: at least one path through all stations is feasible

### Part 2: The greedy algorithm finds it

**Claim**: If we fail at station `j` starting from `i`, the answer is not in `[i, j]`.

**Proof**:
- From `i` to `j-1`, we maintained non-negative tank
- At `j`, tank became negative: tank_j < 0
- For any `k` in `[i+1, j-1]`:
  - tank at k (starting from i) = tank_k ≥ 0
  - If we start at k instead, we miss gain from i to k-1
  - We'd reach j with even less fuel → still fail

**Conclusion**: If solution exists (total ≥ 0), and we reset at failures, the final start position is correct.

---

## Alternative: Minimum Tank Position

Find the position where cumulative tank is minimum.

```python
def can_complete_circuit_v2(gas: list[int], cost: list[int]) -> int:
    """
    Alternative approach: find minimum cumulative point.

    Starting right after the minimum avoids ever going negative.

    Time: O(n)
    Space: O(1)
    """
    n = len(gas)
    total = 0
    min_tank = float('inf')
    min_index = 0

    for i in range(n):
        total += gas[i] - cost[i]
        if total < min_tank:
            min_tank = total
            min_index = i

    if total < 0:
        return -1

    # Start from the station after the minimum point
    return (min_index + 1) % n
```

### Intuition

```
cumulative: -2, -4, -6, -3, 0

Index:       0   1   2   3   4
             ↓       ↓
         min here at 2 (value -6)

Starting at index 3 (after minimum):
- We never revisit the "valley"
- We hit maximum cumulative before returning to start
```

---

## Variations

### 1. Minimum Starting Fuel

Find minimum initial fuel needed to complete circuit starting from index 0.

```python
def min_starting_fuel(gas: list[int], cost: list[int]) -> int:
    """
    Find minimum initial fuel to complete circuit from index 0.

    Time: O(n)
    Space: O(1)
    """
    tank = 0
    min_tank = 0

    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        min_tank = min(min_tank, tank)

    # We need to offset the most negative point
    return max(0, -min_tank)
```

### 2. All Valid Starting Points

Find all stations that work as starting points.

```python
def all_valid_starts(gas: list[int], cost: list[int]) -> list[int]:
    """
    Find all valid starting stations.
    Note: If solution exists, it's unique (unless multiple due to symmetry).

    Time: O(n)
    Space: O(1)
    """
    n = len(gas)
    if sum(gas) < sum(cost):
        return []

    # Standard algorithm finds one
    result = can_complete_circuit(gas, cost)

    # For most cases, only one valid start exists
    # Edge case: all gains are 0 → all starts work
    if all(gas[i] == cost[i] for i in range(n)):
        return list(range(n))

    return [result]
```

### 3. Circular Array Maximum Subarray

Related: find maximum sum of circular subarray.

```python
def max_circular_subarray(nums: list[int]) -> int:
    """
    Maximum sum of circular subarray.

    Key insight: max(normal_kadane, total_sum - min_subarray)

    Time: O(n)
    Space: O(1)
    """
    max_sum = nums[0]
    min_sum = nums[0]
    current_max = nums[0]
    current_min = nums[0]
    total = nums[0]

    for num in nums[1:]:
        total += num
        current_max = max(num, current_max + num)
        max_sum = max(max_sum, current_max)
        current_min = min(num, current_min + num)
        min_sum = min(min_sum, current_min)

    # Handle all-negative case
    if max_sum < 0:
        return max_sum

    # Maximum is either normal subarray or wrap-around
    return max(max_sum, total - min_sum)
```

---

## Why Greedy Works

The problem has both greedy properties:

1. **Greedy Choice**: Starting after a failure point is always as good or better
2. **Optimal Substructure**: If we can complete from `i`, the partial solution from any point is valid

The key insight is the **elimination**: failing at `j` rules out all stations from `i` to `j-1`.

---

## Complexity Analysis

| Operation | Time | Space | Notes |
|-----------|------|-------|-------|
| Basic solution | O(n) | O(1) | Single pass |
| Min cumulative approach | O(n) | O(1) | Track minimum |
| Brute force (comparison) | O(n²) | O(1) | Try each start |

---

## Edge Cases

- [ ] Single station with gas[0] >= cost[0] → return 0
- [ ] Single station with gas[0] < cost[0] → return -1
- [ ] All gas equals cost → any station works
- [ ] Sum(gas) < sum(cost) → return -1
- [ ] Last station is valid start → algorithm handles wrap-around

---

## Practice Problems

| # | Problem | Difficulty | Key Insight |
|---|---------|------------|-------------|
| 1 | Gas Station | Medium | Greedy reset on failure |
| 2 | Maximum Sum Circular Subarray | Medium | Kadane + wrap-around |
| 3 | Minimum Number of Refueling Stops | Hard | Heap-based greedy |
| 4 | Cheapest Flights Within K Stops | Medium | BFS/Bellman-Ford |

---

## Interview Tips

1. **State the two observations**: total sum check + greedy reset
2. **Prove elimination works**: failing at j rules out i to j
3. **Trace an example**: show the reset happening
4. **Handle no solution**: check total_tank at end
5. **Mention uniqueness**: if solution exists, it's unique

---

## Key Takeaways

1. If sum(gas) >= sum(cost), a solution exists
2. Failing at station j means no station from i to j works
3. Single pass O(n) solution by tracking reset points
4. Alternative: start after the cumulative minimum point
5. The solution, if it exists, is unique

---

## Next: [07-candy-distribution.md](./07-candy-distribution.md)

Learn the two-pass greedy pattern with the candy distribution problem.
