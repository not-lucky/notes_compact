# Candy Distribution

> **Prerequisites:** [Greedy Basics](./01-greedy-basics.md)

## Interview Context

Candy distribution tests:
1. **Two-pass greedy**: Forward and backward passes
2. **Constraint satisfaction**: Meeting neighbor requirements
3. **Optimization**: Minimizing total candies
4. **Pattern recognition**: Similar to trapping rain water

---

## Building Intuition

**Why Can't We Solve This in One Pass?**

Each child must have more candy than both neighbors if they have a higher rating. One pass only considers one direction:

```
ratings = [1, 3, 2, 2, 1]

Left-to-right pass (considering left neighbor only):
candies = [1, 2, 1, 1, 1]
           ↑  ↑
           OK: 2 > 1 because 3 > 1
              But wait: rating[2]=2 > rating[4]=1,
              yet candies[2]=1 = candies[4]=1 ✗

We need to also look RIGHT!
```

**The Two-Pass Strategy**

Pass 1: Handle LEFT neighbor relationships
Pass 2: Handle RIGHT neighbor relationships

```
ratings = [1, 3, 2, 2, 1]

Initial:     [1, 1, 1, 1, 1]

Left-to-right (if rating[i] > rating[i-1], candy[i] = candy[i-1] + 1):
i=1: 3 > 1 → candies[1] = 1 + 1 = 2
i=2: 2 < 3 → no change
i=3: 2 = 2 → no change
i=4: 1 < 2 → no change
Result:      [1, 2, 1, 1, 1]

Right-to-left (if rating[i] > rating[i+1], candy[i] = max(candy[i], candy[i+1] + 1)):
i=3: 2 > 1 → candies[3] = max(1, 1+1) = 2
i=2: 2 = 2 → no change
i=1: 3 > 2 → candies[1] = max(2, 1+1) = 2 (already 2)
i=0: 1 < 3 → no change
Result:      [1, 2, 1, 2, 1]

Total: 1 + 2 + 1 + 2 + 1 = 7
```

**Why Take MAX in the Second Pass?**

The second pass might want to DECREASE candy to satisfy the right neighbor, but we can't violate the left neighbor constraint we already satisfied:

```
ratings = [1, 2, 87, 87, 87, 2, 1]

After left-to-right: [1, 2, 3, 1, 1, 1, 1]
                           ↑
                        Rating 87 got 3 candies

Right-to-left at index 4:
- Rating[4]=87 > rating[5]=2 → needs more than candies[5]=2
- candies[4] = max(1, 2+1) = 3

At index 3:
- Rating[3]=87 = rating[4]=87 → no constraint
- candies[3] stays 1

The max() ensures we never violate left constraints while satisfying right ones.
```

**Mental Model: The "Hill" Shape**

Candy distribution creates "hills" where peaks get the most candy:

```
ratings: 1   2   3   2   1
candies: 1   2   3   2   1
             ↑
            Peak

ratings: 1   3   2   1   4   3
candies: 1   2   1   1   2   1
             ↑           ↑
          Peak         Peak

The two-pass approach naturally builds hills from both sides.
```

---

## When NOT to Use Two-Pass

**1. When There Are More Complex Constraints**

If constraints involve more than immediate neighbors:
```
"Child i must have more candy than ALL children within distance 2 if higher rated"

Two-pass won't work—need to track a window or use different approach.
```

**2. When Candy Values Are Constrained**

If candy must be between 1 and k, or must be specific values:
```
This becomes a constraint satisfaction problem,
potentially needing backtracking or linear programming.
```

**3. When You Need Optimal Assignment (Not Just Total)**

If there are multiple valid distributions and you need a specific one:
```
ratings = [1, 1, 1]
Valid:    [1, 1, 1], [2, 1, 1], [1, 1, 2], etc.

Two-pass gives ONE valid answer; finding "all" needs different approach.
```

**4. When Ratings Can Be Modified**

If you can change ratings to minimize total candy:
```
This is an optimization problem over the input, not the output.
```

---

## Problem Statement

`n` children stand in a line with ratings. Distribute candies such that:
1. Each child gets at least 1 candy
2. Children with higher rating than neighbors get more candies

Find the **minimum total candies** needed.

```
Input:  ratings = [1, 0, 2]
Output: 5

Distribution: [2, 1, 2]
- Child 0 (rating 1): more than child 1 → gets 2
- Child 1 (rating 0): minimum → gets 1
- Child 2 (rating 2): more than child 1 → gets 2
Total: 2 + 1 + 2 = 5
```

---

## The Core Insight

**Two passes handle both neighbor constraints**:
1. **Left-to-right**: If `ratings[i] > ratings[i-1]`, give more than left neighbor
2. **Right-to-left**: If `ratings[i] > ratings[i+1]`, give more than right neighbor

Take the maximum of both passes for each child.

```
Why two passes?

One pass can't satisfy both neighbors:
ratings = [1, 2, 2]

Left-to-right only: [1, 2, 1] - child 1 has more than child 0 ✓
                    But child 2 has same rating as child 1, both get different amounts?
                    Actually [1, 2, 1] works here since ratings[2] = ratings[1] (equal)

ratings = [1, 3, 2, 2, 1]

Left-to-right: [1, 2, 1, 1, 1]
- Child 2 should have more than child 4, but doesn't!

Right-to-left: [1, 1, 1, 2, 1]
- Child 1 should have more than child 0, but doesn't!

Combined (max): [1, 2, 1, 2, 1] ✓
```

---

## Solution: Two-Pass Greedy

```python
def candy(ratings: list[int]) -> int:
    """
    Minimum candies to satisfy rating requirements.

    Two passes:
    1. Left-to-right: handle left neighbor constraint
    2. Right-to-left: handle right neighbor constraint

    Time: O(n)
    Space: O(n)
    """
    n = len(ratings)
    if n == 0:
        return 0

    candies = [1] * n

    # Left to right: if higher than left, get one more than left
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            candies[i] = candies[i - 1] + 1

    # Right to left: if higher than right, get at least one more than right
    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i + 1]:
            candies[i] = max(candies[i], candies[i + 1] + 1)

    return sum(candies)
```

---

## Visual Trace

```
ratings = [1, 2, 87, 87, 87, 2, 1]

Initial: candies = [1, 1, 1, 1, 1, 1, 1]

Left-to-right pass:
i=1: ratings[1]=2 > ratings[0]=1 → candies[1] = 1+1 = 2
i=2: ratings[2]=87 > ratings[1]=2 → candies[2] = 2+1 = 3
i=3: ratings[3]=87 = ratings[2]=87 → no change
i=4: ratings[4]=87 = ratings[3]=87 → no change
i=5: ratings[5]=2 < ratings[4]=87 → no change
i=6: ratings[6]=1 < ratings[5]=2 → no change

candies = [1, 2, 3, 1, 1, 1, 1]

Right-to-left pass:
i=5: ratings[5]=2 > ratings[6]=1 → candies[5] = max(1, 1+1) = 2
i=4: ratings[4]=87 > ratings[5]=2 → candies[4] = max(1, 2+1) = 3
i=3: ratings[3]=87 = ratings[4]=87 → no change (still 1)
i=2: ratings[2]=87 = ratings[3]=87 → no change (stays 3)
i=1: ratings[1]=2 < ratings[2]=87 → no change (stays 2)
i=0: ratings[0]=1 < ratings[1]=2 → no change (stays 1)

candies = [1, 2, 3, 1, 3, 2, 1]

Total: 1 + 2 + 3 + 1 + 3 + 2 + 1 = 13
```

---

## One-Pass Solution (Space Optimized)

```python
def candy_one_pass(ratings: list[int]) -> int:
    """
    One-pass solution using slope counting.

    Track up and down slopes, allocate candies accordingly.

    Time: O(n)
    Space: O(1)
    """
    n = len(ratings)
    if n <= 1:
        return n

    total = 1
    up = 0
    down = 0
    peak = 0

    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            # Going up
            up += 1
            down = 0
            peak = up
            total += up + 1
        elif ratings[i] < ratings[i - 1]:
            # Going down
            down += 1
            up = 0
            # If down exceeds peak, need to increase peak candy
            total += down + (1 if down > peak else 0)
        else:
            # Equal ratings
            up = 0
            down = 0
            peak = 0
            total += 1

    return total
```

---

## Why Two-Pass Works

### Greedy Choice Property

Each pass makes locally optimal decisions:
- Left pass: give minimum extra to satisfy left constraint
- Right pass: adjust to satisfy right constraint without violating left

### Optimal Substructure

The solution for ratings[0..i] doesn't affect the solution for ratings[i+1..n].
Each position's candy count depends only on neighbors.

### Proof of Minimum

**Claim**: Two-pass gives minimum candies.

**By construction**:
1. Start with 1 candy per child (minimum possible)
2. Left pass adds exactly what's needed for left constraints
3. Right pass adds exactly what's needed for right constraints
4. Taking max ensures both constraints are met minimally

---

## Related Problems

### Trapping Rain Water (Similar Pattern)

```python
def trap(height: list[int]) -> int:
    """
    Calculate trapped water using two-pass approach.

    Time: O(n)
    Space: O(n)
    """
    n = len(height)
    if n <= 2:
        return 0

    left_max = [0] * n
    right_max = [0] * n

    # Left pass: max height to the left
    left_max[0] = height[0]
    for i in range(1, n):
        left_max[i] = max(left_max[i - 1], height[i])

    # Right pass: max height to the right
    right_max[n - 1] = height[n - 1]
    for i in range(n - 2, -1, -1):
        right_max[i] = max(right_max[i + 1], height[i])

    # Water at each position
    water = 0
    for i in range(n):
        water += min(left_max[i], right_max[i]) - height[i]

    return water
```

### Product of Array Except Self

```python
def product_except_self(nums: list[int]) -> list[int]:
    """
    Product of all elements except self, without division.

    Time: O(n)
    Space: O(1) extra (output doesn't count)
    """
    n = len(nums)
    result = [1] * n

    # Left pass: product of all elements to the left
    prefix = 1
    for i in range(n):
        result[i] = prefix
        prefix *= nums[i]

    # Right pass: multiply by product of all elements to the right
    suffix = 1
    for i in range(n - 1, -1, -1):
        result[i] *= suffix
        suffix *= nums[i]

    return result
```

---

## Two-Pass Pattern Summary

| Problem | Left Pass | Right Pass | Combine |
|---------|-----------|------------|---------|
| Candy | Left neighbor constraint | Right neighbor constraint | Max |
| Trapping Rain Water | Left max height | Right max height | Min - height |
| Product Except Self | Left product | Right product | Multiply |
| Stock Span | Days since higher | (variant) | - |

---

## Complexity Analysis

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Two-pass | O(n) | O(n) | Simple, clear |
| One-pass (slope) | O(n) | O(1) | Tricky logic |
| Brute force | O(n²) | O(n) | Simulate |

---

## Edge Cases

- [ ] Single child → return 1
- [ ] Two children → depends on ratings comparison
- [ ] All same ratings → all get 1 candy
- [ ] Strictly increasing → [1, 2, 3, ..., n]
- [ ] Strictly decreasing → [n, ..., 3, 2, 1]
- [ ] V-shaped (decreasing then increasing) → peak at minimum

---

## Practice Problems

| # | Problem | Difficulty | Key Insight |
|---|---------|------------|-------------|
| 1 | Candy | Hard | Two-pass greedy |
| 2 | Trapping Rain Water | Hard | Two-pass or two-pointer |
| 3 | Product of Array Except Self | Medium | Prefix and suffix products |
| 4 | Container With Most Water | Medium | Two pointers |
| 5 | Increasing Triplet Subsequence | Medium | Track first and second smallest |

---

## Interview Tips

1. **Draw the passes**: Show candies array after each pass
2. **Explain why two passes**: One pass can't handle both neighbors
3. **Trace an example**: Especially with a "valley" in ratings
4. **Mention optimization**: One-pass exists but is trickier
5. **Connect to similar problems**: Trapping rain water uses same pattern

---

## Key Takeaways

1. Two-pass greedy: left-to-right then right-to-left
2. Each pass handles one direction of constraints
3. Combine with max (candy) or min (water) as appropriate
4. O(n) time, O(n) space for simple version
5. Pattern applies to many "neighbor constraint" problems

---

## Next: [08-partition-labels.md](./08-partition-labels.md)

Learn the partition labels problem - interval-based greedy partitioning.
