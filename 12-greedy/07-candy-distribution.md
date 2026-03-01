# Candy Distribution

> **Prerequisites:** [Greedy Basics](./01-greedy-basics.md)

## Interview Context

Candy distribution tests:

1. **Two-pass greedy**: Forward and backward passes to handle bidirectional constraints
2. **Constraint satisfaction**: Meeting neighbor requirements from both sides
3. **Optimization**: Minimizing total candies distributed
4. **Pattern recognition**: Same two-pass structure as Trapping Rain Water and Product Except Self

---

## Problem Statement

`n` children stand in a line, each with a rating. Distribute candies such that:

1. Each child gets **at least 1 candy**.
2. A child with a **higher rating than an immediate neighbor** must get **more candies** than that neighbor.

**Goal:** Find the **minimum total candies** needed to satisfy all constraints.

**Key clarification:** Children with equal ratings have no constraint relative to each other -- they can receive the same or different candy counts.

```text
Input:  ratings = [1, 0, 2]
Output: 5

Distribution: [2, 1, 2]
- Child 0 (rating 1): higher than child 1 (rating 0) -> gets 2 > 1
- Child 1 (rating 0): lowest -> gets 1 (minimum)
- Child 2 (rating 2): higher than child 1 (rating 0) -> gets 2 > 1
Total: 2 + 1 + 2 = 5
```

---

## Building Intuition

### Why Can't We Solve This in One Pass?

A single pass only considers one direction at a time, so it cannot simultaneously satisfy both left and right neighbor constraints:

```text
ratings = [1, 3, 2, 2, 1]

Left-to-right pass (considering left neighbor only):
candies = [1, 2, 1, 1, 1]
                      ^  ^
               rating[3]=2 > rating[4]=1,
               yet candies[3]=1 == candies[4]=1  VIOLATED

We need to also look RIGHT!
```

### The Two-Pass Strategy

- **Pass 1 (left-to-right)**: Satisfy all LEFT neighbor constraints.
- **Pass 2 (right-to-left)**: Satisfy all RIGHT neighbor constraints, without breaking the left ones.

```text
ratings = [1, 3, 2, 2, 1]

Step 0 - Initialize:  [1, 1, 1, 1, 1]  (everyone starts with 1)

Step 1 - Left-to-right (if rating[i] > rating[i-1], candy[i] = candy[i-1] + 1):
  i=1: 3 > 1 -> candies[1] = 1 + 1 = 2
  i=2: 2 < 3 -> no change
  i=3: 2 = 2 -> no change
  i=4: 1 < 2 -> no change
  Result:         [1, 2, 1, 1, 1]

Step 2 - Right-to-left (if rating[i] > rating[i+1], candy[i] = max(candy[i], candy[i+1] + 1)):
  i=3: 2 > 1 -> candies[3] = max(1, 1+1) = 2
  i=2: 2 = 2 -> no change
  i=1: 3 > 2 -> candies[1] = max(2, 1+1) = 2  (no change, left pass already set it)
  i=0: 1 < 3 -> no change
  Result:         [1, 2, 1, 2, 1]

Total: 1 + 2 + 1 + 2 + 1 = 7
```

### Why Take `max` in the Second Pass?

The right-to-left pass must satisfy the right-neighbor constraint **without breaking** the left-neighbor constraint already established. Using `max()` picks the larger value needed to satisfy both constraints simultaneously:

```text
ratings = [1, 2, 87, 87, 87, 2, 1]

After left-to-right: [1, 2, 3, 1, 1, 1, 1]
                            ^
                         Index 2: left pass gave 3 candies

Right-to-left at index 4:
  rating[4]=87 > rating[5]=2 -> candies[4] = max(1, 1+1) = 2  (was 1, needs 2)

Right-to-left at index 2:
  rating[2]=87 = rating[3]=87 -> no constraint
  candies[2] stays 3  (left pass value PRESERVED by max)

Without max(), the right pass might overwrite index 2 to a smaller value,
breaking the left-neighbor constraint (rating[2]=87 > rating[1]=2).
```

### Mental Model: The "Hill" Shape

Visualize the ratings as a landscape of hills and valleys. The two-pass approach builds candy "hills" from both directions. Each child's candy count equals its height in the taller hill:

```text
ratings: 1   2   3   2   1          ratings: 1   3   2   1   4   3
candies: 1   2   3   2   1          candies: 1   3   2   1   2   1
                 ^                               ^           ^
              Peak                            Peak         Peak

Each peak gets the maximum candy count for its hill.
Valleys (local minima) always get 1 candy.
```

---

## Solution: Two-Pass Greedy

```python
def candy(ratings: list[int]) -> int:
    """
    Minimum candies to satisfy neighbor rating constraints.

    Pass 1: left-to-right handles left neighbor constraint.
    Pass 2: right-to-left handles right neighbor constraint.
    max() merges both constraints without violating either.

    Time:  O(n)
    Space: O(n)
    """
    n = len(ratings)
    if n == 0:
        return 0

    candies = [1] * n

    # Pass 1: each child with a higher rating than their left neighbor
    # must get more candy than that neighbor
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            candies[i] = candies[i - 1] + 1

    # Pass 2: each child with a higher rating than their right neighbor
    # must get more candy than that neighbor.
    # max() preserves left-pass constraints.
    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i + 1]:
            candies[i] = max(candies[i], candies[i + 1] + 1)

    return sum(candies)
```

---

## Visual Trace

```text
ratings = [1, 2, 87, 87, 87, 2, 1]

Initial: candies = [1, 1, 1, 1, 1, 1, 1]

LEFT-TO-RIGHT PASS (only check left neighbor):
  i=1: ratings[1]=2  > ratings[0]=1  -> candies[1] = 1+1 = 2
  i=2: ratings[2]=87 > ratings[1]=2  -> candies[2] = 2+1 = 3
  i=3: ratings[3]=87 = ratings[2]=87 -> no change
  i=4: ratings[4]=87 = ratings[3]=87 -> no change
  i=5: ratings[5]=2  < ratings[4]=87 -> no change
  i=6: ratings[6]=1  < ratings[5]=2  -> no change

  candies = [1, 2, 3, 1, 1, 1, 1]
             -------^               left constraints satisfied
                     ^-----------   right constraints NOT yet handled

RIGHT-TO-LEFT PASS (only check right neighbor, merge with max):
  i=5: ratings[5]=2  > ratings[6]=1  -> candies[5] = max(1, 1+1) = 2
  i=4: ratings[4]=87 > ratings[5]=2  -> candies[4] = max(1, 2+1) = 3
  i=3: ratings[3]=87 = ratings[4]=87 -> no change (stays 1)
  i=2: ratings[2]=87 = ratings[3]=87 -> no change (stays 3, left value preserved)
  i=1: ratings[1]=2  < ratings[2]=87 -> no change (stays 2)
  i=0: ratings[0]=1  < ratings[1]=2  -> no change (stays 1)

  candies = [1, 2, 3, 1, 3, 2, 1]

VERIFY ALL CONSTRAINTS:
  i=0: rating 1  < rating 2  (right) -> no constraint               OK
  i=1: rating 2  > rating 1  (left)  -> candy 2 > 1                 OK
       rating 2  < rating 87 (right) -> no constraint               OK
  i=2: rating 87 > rating 2  (left)  -> candy 3 > 2                 OK
       rating 87 = rating 87 (right) -> no constraint               OK
  i=3: rating 87 = rating 87 (left)  -> no constraint               OK
       rating 87 = rating 87 (right) -> no constraint               OK
  i=4: rating 87 = rating 87 (left)  -> no constraint               OK
       rating 87 > rating 2  (right) -> candy 3 > 2                 OK
  i=5: rating 2  < rating 87 (left)  -> no constraint               OK
       rating 2  > rating 1  (right) -> candy 2 > 1                 OK
  i=6: rating 1  < rating 2  (left)  -> no constraint               OK

Total: 1 + 2 + 3 + 1 + 3 + 2 + 1 = 13
```

---

## One-Pass Solution (Space Optimized)

Instead of storing the entire `candies` array, we can track the shape of ascending and descending "slopes" in the ratings and compute the total on the fly.

**Key idea:** The candy distribution for any sequence of ratings decomposes into ascending runs, descending runs, and flat segments. We can compute each run's contribution arithmetically.

- **Ascending run of length `k`**: contributes `1 + 2 + ... + k` candies.
- **Descending run of length `k`**: also contributes `1 + 2 + ... + k` candies (assigned in reverse).
- **Peak handling**: If a descending run grows longer than the preceding ascending run, the peak child needs an extra candy (bumped retroactively).

```python
def candy_one_pass(ratings: list[int]) -> int:
    """
    One-pass solution using slope counting.

    Tracks ascending/descending runs in the ratings.
    When a descent exceeds the preceding ascent, the peak
    is retroactively bumped by 1.

    Time:  O(n)
    Space: O(1)
    """
    n = len(ratings)
    if n <= 1:
        return n

    total = 1  # First child always gets 1 candy
    up = 0     # Length of current ascending run
    down = 0   # Length of current descending run
    peak = 0   # Length of ascending run at the most recent peak

    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            # Ascending: extend the upward slope
            up += 1
            down = 0
            peak = up
            total += up + 1  # This child gets (up + 1) candies

        elif ratings[i] < ratings[i - 1]:
            # Descending: extend the downward slope
            down += 1
            up = 0
            # Each step down adds `down` to total:
            #   - New bottom child gets 1 candy
            #   - Every child above on the slope gets +1 (shifting up)
            # If descent exceeds ascent, the peak also shifts up by 1
            total += down + (1 if down > peak else 0)

        else:
            # Equal ratings: no constraint, reset slopes
            up = 0
            down = 0
            peak = 0
            total += 1  # This child gets minimum 1 candy

    return total
```

### How Slope Counting Works

Consider a descending run `[5, 4, 3, 2, 1]`. The candy assignment must be `[5, 4, 3, 2, 1]` (or equivalently, 5 candies for the highest, 1 for the lowest). Each time we extend the descent by one step, every child already on the slope needs one more candy to maintain the strictly decreasing constraint:

```text
Step 1: ratings so far [5, 4]       -> candies [2, 1]          total += 2
Step 2: ratings so far [5, 4, 3]    -> candies [3, 2, 1]       total += 3 (shift up + new bottom)
Step 3: ratings so far [5, 4, 3, 2] -> candies [4, 3, 2, 1]    total += 4
Step 4: ratings so far [5,4,3,2,1]  -> candies [5, 4, 3, 2, 1] total += 5

Notice a pattern:
At Step 2, `down` is 2. We add `down` (2) to the total. Wait, why?
Because the new total (6) - old total (3) = 3.
At Step 3, `down` is 3. We add 3 to the total.
At Step 4, `down` is 4. We add 4 to the total.

Each step adds exactly `down` to the total because we shift the existing `down-1` children up by 1 (taking `down-1` candies) and add 1 new child at the bottom (taking 1 candy). So `(down-1) + 1 = down` new candies are added to the total.
```

### One-Pass Visual Trace

```text
ratings = [1, 2, 3, 2, 1]

i=0: Start. total=1, up=0, down=0, peak=0
     Candies so far: [1]

i=1: 2 > 1 (ascending)
     up=1, down=0, peak=1
     total += 1+1 = 2 -> total=3
     Candies so far: [1, 2]

i=2: 3 > 2 (ascending)
     up=2, down=0, peak=2
     total += 2+1 = 3 -> total=6
     Candies so far: [1, 2, 3]

i=3: 2 < 3 (descending)
     down=1, up=0
     down(1) <= peak(2): no peak bump
     total += 1 + 0 = 1 -> total=7
     Candies so far: [1, 2, 3, 2]
                                ^-- descent step 1: child gets 2? No...

     Wait -- the descent assigns candies in reverse. After the full
     descent is processed, the children on the down-slope get
     [down, down-1, ..., 1] candies. At this moment with down=1,
     the child at i=3 gets 1 candy. The +1 added to total represents
     that 1 candy. But won't it need to become 2 later? Yes -- if the
     descent continues, the NEXT step will shift this child up.

i=4: 1 < 2 (descending)
     down=2, up=0
     down(2) <= peak(2): no peak bump
     total += 2 + 0 = 2 -> total=9
     Candies so far: [1, 2, 3, 2, 1]
                                ^--^-- child at i=3 shifted up to 2, child at i=4 gets 1

Final: total = 9
Candy distribution: [1, 2, 3, 2, 1]
```

### Trace with Peak Adjustment

When the descending run grows longer than the ascending run, the peak child must be bumped:

```text
ratings = [1, 2, 3, 2, 1, 0]

i=0..2 (ascending): total=6, up=2, peak=2
  Candies: [1, 2, 3]

i=3: 2 < 3 (descending), down=1
  down(1) <= peak(2): no bump
  total += 1 = 7
  Candies: [1, 2, 3, 1]

i=4: 1 < 2 (descending), down=2
  down(2) <= peak(2): no bump
  total += 2 = 9
  Candies: [1, 2, 3, 2, 1]

i=5: 0 < 1 (descending), down=3
  down(3) > peak(2): PEAK BUMP! Add extra +1
  total += 3 + 1 = 13
  Candies: [1, 2, 4, 3, 2, 1]
                ^
           Peak bumped from 3 to 4!

Without the bump, the peak (index 2) would have 3 candies
and the descent would need [3, 2, 1] -- but that requires
the peak to be at least 4 to stay above the descent.

Final: total = 13
```

---

## Why Two-Pass Works

### Greedy Choice Property

Each pass makes locally optimal decisions:

- **Left pass**: Give the minimum extra candy needed to satisfy the left constraint.
- **Right pass**: Adjust candy to satisfy the right constraint without violating the left.

### Optimal Substructure

Each child's minimum candy count depends on two independent values:
1. The length of the strictly increasing run ending at that child **from the left**.
2. The length of the strictly increasing run ending at that child **from the right**.

These are computed independently per direction, then combined with `max()`.

### Proof of Minimum

**Claim**: Two-pass gives the minimum total candies.

**Proof sketch**:

1. **Lower bound**: Each child must receive at least `max(left_run, right_run)` candies, where `left_run` is 1 + the length of the strictly increasing run to the left, and `right_run` is 1 + the length of the strictly increasing run to the right. Any smaller value would violate at least one neighbor constraint.

2. **Achievability**: The two-pass algorithm assigns exactly `max(left_run, right_run)` to each child. The left pass computes `left_run` and the right pass computes `right_run`. Using `max()` combines them.

3. **Therefore**: The two-pass assignment equals the lower bound at every position, so it is minimum.

---

## Common Mistakes

### 1. Forgetting to Use `max()` in the Second Pass

```python
# WRONG: Overwrites left-pass constraints
if ratings[i] > ratings[i + 1]:
    candies[i] = candies[i + 1] + 1  # BUG: loses left-pass info

# CORRECT: Preserves both constraints
if ratings[i] > ratings[i + 1]:
    candies[i] = max(candies[i], candies[i + 1] + 1)
```

### 2. Treating Equal Ratings as a Constraint

```python
# WRONG: >= instead of >
if ratings[i] >= ratings[i - 1]:  # BUG: equal ratings don't require more candy
    candies[i] = candies[i - 1] + 1

# CORRECT: Only strict inequality creates constraints
if ratings[i] > ratings[i - 1]:
    candies[i] = candies[i - 1] + 1
```

### 3. Incorrect Loop Bounds in Right-to-Left Pass

```python
# WRONG: Stops at 1, misses index 0
for i in range(n - 2, 0, -1):

# WRONG: ratings[i+1] goes out of bounds at i=n-1
for i in range(n - 1, -1, -1):

# CORRECT: Start at n-2 (last index that has a right neighbor), go down to 0
for i in range(n - 2, -1, -1):
```

### 4. Not Initializing with 1 Candy Each

```python
# WRONG: Starting with 0 candies
candies = [0] * n  # BUG: violates "at least 1 candy" rule

# CORRECT: Everyone starts with 1
candies = [1] * n
```

---

## When NOT to Use Two-Pass

**1. Constraints beyond immediate neighbors.** If a child must have more candy than all children within distance `k`, two-pass won't suffice -- need sliding window or different approach.

**2. Bounded candy values.** If candy must be between 1 and `k`, run two-pass first, then check if any value exceeds `k`. If so, no valid assignment exists (since two-pass gives the minimum).

**3. Circular arrangement.** If the first and last children are neighbors, the wrap-around dependency makes simple two-pass insufficient. You need to iterate passes until convergence or find a starting point that avoids wrap-around conflicts.

**4. Enumerating all valid assignments.** Two-pass gives the unique minimum-total answer. Enumerating all valid distributions requires a different approach.

---

## Problem Variations

### Variation 1: Circular Arrangement

Children stand in a circle (first and last are neighbors). The wrap-around dependency means a single two-pass is not enough -- updating one end can invalidate the other.

**Correct approach**: Iterate passes until no changes occur.

```python
def candy_circular(ratings: list[int]) -> int:
    """
    Candy distribution where children form a circle.

    Iterate forward and backward passes until stable.
    Each pass only increases values, so convergence is guaranteed.
    Since changes propagate strictly left-to-right or right-to-left
    during a pass, and we do both in each loop iteration, the while loop
    executes at most O(n) times. The worst case happens when changes
    must propagate sequentially around the circle.

    Time:  O(n^2) worst case
    Space: O(n)
    """
    n = len(ratings)
    if n <= 1:
        return n

    candies = [1] * n
    changed = True

    while changed:
        changed = False

        # Forward pass
        for i in range(n):
            left = (i - 1) % n
            if ratings[i] > ratings[left] and candies[i] <= candies[left]:
                candies[i] = candies[left] + 1
                changed = True

        # Backward pass
        for i in range(n - 1, -1, -1):
            right = (i + 1) % n
            if ratings[i] > ratings[right] and candies[i] <= candies[right]:
                candies[i] = candies[right] + 1
                changed = True

    return sum(candies)
```

### Variation 2: Bounded Candy Values

Each child must receive between 1 and `k` candies. If the two-pass minimum exceeds `k` for any child, no valid assignment exists.

```python
def candy_bounded(ratings: list[int], k: int) -> int:
    """Return minimum total candies, or -1 if no valid assignment within [1, k]."""
    n = len(ratings)
    if n == 0:
        return 0

    candies = [1] * n
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            candies[i] = candies[i - 1] + 1
    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i + 1]:
            candies[i] = max(candies[i], candies[i + 1] + 1)

    if max(candies) > k:
        return -1  # Two-pass gives minimum; if it exceeds k, impossible
    return sum(candies)
```

---

## Related Problems: The Two-Pass Pattern

The two-pass pattern appears whenever you need to combine information from both directions. Here are two classic examples that share this structure.

### Trapping Rain Water (Two-Pass)

```python
def trap(height: list[int]) -> int:
    """
    Water trapped at each bar = min(left_max, right_max) - height.

    Time:  O(n)
    Space: O(n)
    """
    n = len(height)
    if n <= 2:
        return 0

    left_max = [0] * n
    right_max = [0] * n

    # Left pass: tallest bar to the left of (or at) each position
    left_max[0] = height[0]
    for i in range(1, n):
        left_max[i] = max(left_max[i - 1], height[i])

    # Right pass: tallest bar to the right of (or at) each position
    right_max[n - 1] = height[n - 1]
    for i in range(n - 2, -1, -1):
        right_max[i] = max(right_max[i + 1], height[i])

    return sum(min(left_max[i], right_max[i]) - height[i] for i in range(n))
```

### Product of Array Except Self (Two-Pass)

```python
def product_except_self(nums: list[int]) -> list[int]:
    """
    Product of all elements except self, without division.

    Time:  O(n)
    Space: O(1) extra (output array not counted)
    """
    n = len(nums)
    result = [1] * n

    # Left pass: prefix product of everything to the left
    prefix = 1
    for i in range(n):
        result[i] = prefix
        prefix *= nums[i]

    # Right pass: multiply by suffix product of everything to the right
    suffix = 1
    for i in range(n - 1, -1, -1):
        result[i] *= suffix
        suffix *= nums[i]

    return result
```

### Two-Pass Pattern Summary

| Problem | Left Pass | Right Pass | Combine |
| :--- | :--- | :--- | :--- |
| **Candy** | Left neighbor constraint | Right neighbor constraint | `max(L, R)` |
| **Trapping Rain Water** | Left max height | Right max height | `min(L, R) - height` |
| **Product Except Self** | Left prefix product | Right suffix product | `L * R` |

---

## Complexity Analysis

| Approach | Time | Space | Notes |
| :--- | :--- | :--- | :--- |
| **Two-pass** | $O(n)$ | $O(n)$ | Simple, clear, recommended for interviews |
| **One-pass (slope)** | $O(n)$ | $O(1)$ | Tricky peak-bump logic; good follow-up optimization |
| **Circular variation** | $O(n^2)$ | $O(n)$ | Iterate until no changes; bounds to $O(n)$ iterations |

---

## Edge Cases

- **Empty array**: Return 0. Handled by `if n == 0`.
- **Single child**: Return 1. Loop bounds naturally handle this.
- **Two children**: `[1, 2]` -> `[1, 2]`; `[2, 1]` -> `[2, 1]`; `[2, 2]` -> `[1, 1]`.
- **All same ratings**: Everyone gets 1. `[2, 2, 2]` -> `[1, 1, 1]`.
- **Strictly increasing**: `[1, 2, 3, ..., n]` -> `[1, 2, 3, ..., n]`.
- **Strictly decreasing**: `[n, ..., 2, 1]` -> `[n, ..., 2, 1]`.
- **V-shaped**: `[3, 2, 1, 2, 3]` -> `[3, 2, 1, 2, 3]`. Valley gets 1; slopes increase outward.
- **Peak in middle**: `[1, 2, 3, 2, 1]` -> `[1, 2, 3, 2, 1]`. Peak gets the most.
- **Plateau**: `[1, 2, 2, 2, 1]` -> `[1, 2, 1, 2, 1]`. Equal ratings break the chain; interior children of a plateau can get 1.

---

## Practice Problems

| # | Problem | Difficulty | Key Insight |
| :--- | :--- | :--- | :--- |
| 1 | [Candy](https://leetcode.com/problems/candy/) (LC 135) | Hard | Two-pass greedy, `max()` to merge constraints |
| 2 | [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) (LC 42) | Hard | Two-pass or two-pointer |
| 3 | [Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/) (LC 238) | Medium | Prefix and suffix products |
| 4 | [Minimum Number of Coins for Fruits](https://leetcode.com/problems/minimum-number-of-coins-for-fruits/) (LC 2944) | Medium | Forward-pass greedy with sliding window / Monotonic Queue |
| 5 | [Distribute Candies Among Children II](https://leetcode.com/problems/distribute-candies-among-children-ii/) (LC 2929) | Medium | Distribution with upper bounds, Math / Combinatorics |

---

## Interview Tips

1. **Start with the two-pass approach.** It is clean, correct, and easy to explain. Save the one-pass optimization for a follow-up.
2. **Draw the passes.** Show the `candies` array after each pass to demonstrate correctness.
3. **Explain WHY two passes.** Prove that a single pass can't handle both neighbor directions.
4. **Trace a non-trivial example.** Use a hill shape like `[1, 3, 2]` or a plateau like `[1, 2, 2, 1]` to show the algorithm handles tricky spots.
5. **Connect to the pattern.** Recognizing the two-pass structure in Trapping Rain Water is a strong signal to interviewers.

---

## Key Takeaways

1. **Two-pass greedy**: Left-to-right then right-to-left, merged with `max()`.
2. **Each pass handles one direction** of neighbor constraints independently.
3. **`max()` is the key**: It merges both directions without violating either.
4. **$O(n)$ time, $O(n)$ space** for the standard version; $O(1)$ space possible with slope counting.
5. **The two-pass pattern** applies broadly: Candy, Trapping Rain Water, Product Except Self.

---

## Next: [08-partition-labels.md](./08-partition-labels.md)

Learn the partition labels problem -- interval-based greedy partitioning.
