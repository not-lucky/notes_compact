# Random Sampling

> **Prerequisites:** [Prefix Sums](../02-arrays-strings/06-prefix-sum.md), [Binary Search](../10-binary-search/README.md) (for weighted selection)

## Building Intuition

**The "Fair Lottery" Mental Model**

Imagine you're running a lottery where people buy tickets as they arrive, but you don't know how many will show up:

- You can only hold `k` winning tickets in your hand
- You must be fair — everyone has an equal chance of winning
- You can't go back to earlier tickets

Reservoir sampling solves this: keep `k` items, and as new ones arrive, randomly decide whether to swap one in.

**Why the Math Works (Reservoir Sampling, k=1)**

For selecting 1 item from n:

- Keep the first item (probability 1)
- On item `i`, replace the current item with probability `1/i`

After all n items, the probability that any specific item `k` is the final selection:

```
P(item k is final) = P(picked at step k) × P(survived all later replacements)
                   = (1/k) × (k/(k+1)) × ((k+1)/(k+2)) × ... × ((n-1)/n)
                                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                          telescoping product — everything cancels
                   = 1/n ✓
```

Each item has exactly `1/n` chance — perfectly fair! The product telescopes because
each numerator cancels with the previous denominator.

**Why the Math Works (Reservoir Sampling, general k)**

For selecting k items from n, on the i-th element (0-indexed, i >= k), we generate
`j = randint(0, i)` and include the item if `j < k` (probability `k/(i+1)`).

Proof that each of the n items ends up in the reservoir with probability `k/n`:

```
For item at index i (0-indexed):
- If i < k: item is placed in the reservoir initially.
  It survives if it's never replaced by any later item.
  P(survives) = k/(k+1) × (k+1)/(k+2) × ... × (n-1)/n = k/n ✓

- If i >= k: item is picked with probability k/(i+1).
  It survives all later steps: (i+1)/(i+2) × ... × (n-1)/n = (i+1)/n.
  P(in reservoir) = k/(i+1) × (i+1)/n = k/n ✓
```

**Fisher-Yates: The Perfect Shuffle**

A **naive** (biased) shuffle: `for each i, pick random j from [0, n), swap arr[i] and arr[j]`.
This generates `n^n` equally-likely random choices, but there are only `n!` permutations.
Since `n^n` is not divisible by `n!` for n >= 3, some permutations are more likely than others.

**Fisher-Yates**: `for i from n-1 down to 1, pick j from [0, i], swap arr[i] and arr[j]`.
This generates exactly `n!` equally-likely outcomes — one per permutation. The key insight
is **shrinking the random range** at each step so each position is decided exactly once.

---

## Interview Context

Random sampling algorithms appear when:

- Selecting random elements from a stream of unknown size
- Shuffling arrays fairly
- Generating random permutations
- Weighted random selection
- Sampling random points from geometric regions
- Monte Carlo algorithms (e.g., estimating pi, randomized testing)

Key algorithms: **Reservoir Sampling** (O(1) space from streams) and **Fisher-Yates Shuffle** (perfect uniformity).

---

## Pattern: Reservoir Sampling

Select k random elements from a stream of unknown or very large size, where you can only make one pass and have limited memory.

### Key Insight

```
For selecting 1 element from n items:
- Keep the first item
- For each subsequent item i (1-indexed):
  - Replace current with probability 1/i

After n items, each has probability 1/n of being selected.

Proof for item i:
P(item i selected) = P(picked at step i) × P(not replaced after)
                   = (1/i) × (i/(i+1)) × ((i+1)/(i+2)) × ... × ((n-1)/n)
                   = 1/n  ✓
```

### Visualization

```
Stream: [5, 2, 8, 1, 9, 3]  (pick 1 random element)

i=1: result = 5       (always keep first — prob 1/1)
i=2: randint(1,2) → say 1 → REPLACE → result = 2    (prob 1/2)
i=3: randint(1,3) → say 3 → KEEP    → result = 2    (prob 1/3 to replace)
i=4: randint(1,4) → say 1 → REPLACE → result = 1    (prob 1/4 to replace)
i=5: randint(1,5) → say 4 → KEEP    → result = 1    (prob 1/5 to replace)
i=6: randint(1,6) → say 6 → KEEP    → result = 1    (prob 1/6 to replace)

Final: 1  (each of 6 elements had exactly 1/6 chance)
```

---

## Implementation

### Reservoir Sampling: Pick 1 Random Element

```python
import random

def reservoir_sample_one(stream):
    """
    Select one random element from a stream using O(1) space.

    Each element has equal probability 1/n of being selected,
    where n is the (unknown) total number of elements.
    Returns None if the stream is empty.

    Time: O(n) — single pass through stream
    Space: O(1)
    """
    result = None

    for i, item in enumerate(stream, 1):  # 1-indexed count
        # With probability 1/i, replace result with current item
        if random.randint(1, i) == 1:
            result = item

    return result


# Test
stream = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
counts = {}
trials = 100_000
for _ in range(trials):
    result = reservoir_sample_one(iter(stream))
    counts[result] = counts.get(result, 0) + 1

# Each should be ~10% of trials
for k in sorted(counts):
    print(f"{k}: {counts[k]} ({counts[k] / trials * 100:.1f}%)")
```

### Reservoir Sampling: Pick k Random Elements

```python
import random

def reservoir_sample_k(stream, k: int) -> list:
    """
    Select k random elements from a stream using O(k) space.

    Algorithm (Vitter's Algorithm R):
    1. Fill reservoir with first k items.
    2. For each subsequent item at 0-indexed position i (i >= k),
       generate j = randint(0, i). If j < k, replace reservoir[j].

    Why it works: Each item ends up in the reservoir with probability
    k/n (see proof in Building Intuition section).

    Time: O(n)
    Space: O(k)
    """
    reservoir = []

    for i, item in enumerate(stream):
        if i < k:
            # Fill reservoir with first k items
            reservoir.append(item)
        else:
            # Include new item with probability k/(i+1)
            j = random.randint(0, i)
            if j < k:
                reservoir[j] = item

    return reservoir


# Test
stream = range(1, 101)  # 1 to 100
sample = reservoir_sample_k(iter(stream), 5)
print(sample)  # 5 random elements from 1-100
```

---

## Problem 1: Linked List Random Node (LeetCode 382) [Medium]

Given a singly linked list, return a random node's value with equal probability.
You don't know the length of the list ahead of time — classic reservoir sampling.

```python
import random

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def __init__(self, head: ListNode):
        self.head = head

    def getRandom(self) -> int:
        """
        Return a random node's value using reservoir sampling (k=1).

        Why reservoir sampling? We could pre-compute the length, but
        reservoir sampling handles it in a single pass with O(1) space.

        Time: O(n) per call
        Space: O(1)
        """
        result = self.head.val
        node = self.head.next
        i = 2  # We've already "seen" the first node

        while node:
            # Replace result with probability 1/i
            if random.randint(1, i) == 1:
                result = node.val
            node = node.next
            i += 1

        return result


# Usage
# head = ListNode(1, ListNode(2, ListNode(3)))
# solution = Solution(head)
# print(solution.getRandom())  # 1, 2, or 3 with equal probability
```

---

## Pattern: Fisher-Yates Shuffle

Generate a uniformly random permutation of an array in-place.

### Algorithm

```
For i from n-1 down to 1:
    j = random integer from 0 to i (inclusive)
    swap arr[i] and arr[j]
```

### Visualization

```
Array: [1, 2, 3, 4]

i=3: j = rand(0..3), say 1 → swap arr[3], arr[1] → [1, 4, 3, 2]
i=2: j = rand(0..2), say 0 → swap arr[2], arr[0] → [3, 4, 1, 2]
i=1: j = rand(0..1), say 1 → swap arr[1], arr[1] → [3, 4, 1, 2]

Result: [3, 4, 1, 2] (one of 24 equally likely permutations)
```

### Why Fisher-Yates is Uniform

```
Step 1 (i=n-1): Choose from n elements for last position    → n choices
Step 2 (i=n-2): Choose from n-1 remaining for second-last   → n-1 choices
...
Step n-1 (i=1): Choose from 2 remaining for second position → 2 choices
Step n   (i=0): Only 1 element left for first position       → 1 choice

Total distinct outcomes: n × (n-1) × ... × 2 × 1 = n!
```

Since there are exactly `n!` permutations and the algorithm generates exactly `n!`
equally-likely outcomes, each permutation has probability `1/n!`. No permutation
is favored — this is a **uniform** distribution over all permutations.

**Contrast with the naive (biased) shuffle:**

```
Naive: for each of n positions, choose from n options → n^n total outcomes
       n^n is NOT divisible by n! for n ≥ 3
       → some permutations map to more outcomes than others → BIASED

Example (n=3): n^n = 27 outcomes, n! = 6 permutations
               27 / 6 = 4.5 — not an integer, so distribution is uneven!
```

---

## Implementation

### Fisher-Yates Shuffle (In-Place)

```python
import random

def shuffle(arr: list) -> list:
    """
    Shuffle array in-place using the Fisher-Yates algorithm.

    At each step i, we pick a random element from the "unshuffled"
    portion [0..i] and swap it into position i, finalizing that position.

    Time: O(n)
    Space: O(1) — in-place
    """
    for i in range(len(arr) - 1, 0, -1):
        j = random.randint(0, i)  # j in [0, i] inclusive
        arr[i], arr[j] = arr[j], arr[i]
    return arr


# Test
arr = [1, 2, 3, 4, 5]
print(shuffle(arr))  # Random permutation
```

### Problem 2: Shuffle an Array (LeetCode 384) [Medium]

```python
import random

class Solution:
    def __init__(self, nums: list[int]):
        self.original = nums[:]
        self.array = nums

    def reset(self) -> list[int]:
        """Return array to original configuration."""
        self.array = self.original[:]
        return self.array

    def shuffle(self) -> list[int]:
        """Return a random shuffling of the array using Fisher-Yates."""
        n = len(self.array)
        for i in range(n - 1, 0, -1):
            j = random.randint(0, i)
            self.array[i], self.array[j] = self.array[j], self.array[i]
        return self.array


# Usage
# sol = Solution([1, 2, 3])
# sol.shuffle()  # Random permutation
# sol.reset()    # Back to [1, 2, 3]
```

---

## Pattern: Weighted Random Selection

Select an element where each has a different probability proportional to its weight.

### Key Insight

Build a **prefix sum** array of weights. To pick, generate a random number in
`[1, total_weight]` and binary search for where it falls in the prefix sums.
Each index "owns" a range proportional to its weight.

```
weights = [1, 3, 2]
prefix  = [1, 4, 6]

Random target in [1, 6]:
  target ∈ [1, 1] → index 0  (1/6 chance)
  target ∈ [2, 4] → index 1  (3/6 chance)
  target ∈ [5, 6] → index 2  (2/6 chance)

Use bisect_left on prefix to find the correct index in O(log n).
```

**Why `bisect_left` is correct:** The prefix array is `[1, 4, 6]`. For `target=1`,
`bisect_left` returns 0. For `target=2`, it returns 1. For `target=4`, it returns 1
(leftmost position where 4 fits). For `target=5`, it returns 2. This exactly
matches the ranges each index "owns."

### Using Prefix Sums

```python
import random
import bisect

class WeightedRandom:
    """
    Select elements with probability proportional to their weights.

    Example: weights = [1, 3, 2], total = 6
      P(index 0) = 1/6 ≈ 16.7%
      P(index 1) = 3/6 = 50.0%
      P(index 2) = 2/6 ≈ 33.3%
    """

    def __init__(self, weights: list[int]):
        """
        Build prefix sum array from weights.
        All weights must be positive.

        Time: O(n)
        Space: O(n)
        """
        self.prefix = []
        running_sum = 0
        for w in weights:
            running_sum += w
            self.prefix.append(running_sum)
        self.total = running_sum

    def pick(self) -> int:
        """
        Return random index with probability proportional to weight.

        Time: O(log n) — binary search
        Space: O(1)
        """
        target = random.randint(1, self.total)
        return bisect.bisect_left(self.prefix, target)


# Test
wr = WeightedRandom([1, 3, 2])  # 1:3:2 ratio
counts = {0: 0, 1: 0, 2: 0}
for _ in range(60000):
    counts[wr.pick()] += 1
print(counts)  # Should be roughly {0: 10000, 1: 30000, 2: 20000}
```

---

## Problem 3: Random Pick with Weight (LeetCode 528) [Medium]

Given an array `w` of positive integers where `w[i]` describes the weight of index `i`,
implement `pickIndex()` which randomly picks an index proportional to its weight.

```python
import random
import bisect

class Solution:
    def __init__(self, w: list[int]):
        # Build prefix sums: prefix[i] = w[0] + w[1] + ... + w[i]
        self.prefix = []
        running = 0
        for weight in w:
            running += weight
            self.prefix.append(running)
        self.total = running

    def pickIndex(self) -> int:
        # Pick random target in [1, total], find which "bucket" it falls in
        target = random.randint(1, self.total)
        return bisect.bisect_left(self.prefix, target)


# Usage
# weights = [1, 3]
# sol = Solution(weights)
# Over many calls, pickIndex() returns 0 about 1/4 of the time, 1 about 3/4
```

---

## Pattern: Random Pick with Blacklist

Select uniformly from `[0, n)` excluding a blacklist, with O(1) pick time.

**Key Insight:** We want to pick from `n - B` valid numbers (where B = blacklist size).
If we only pick from `[0, n - B)`, some blacklisted numbers fall in that range. We remap
each such blacklisted number to a non-blacklisted number in `[n - B, n)`.

```
Example: n = 7, blacklist = [2, 3, 5]
Valid range: [0, 4)  (size = 7 - 3 = 4)
Blacklisted in valid range: 2, 3
Non-blacklisted at the end: 4, 6  (5 is blacklisted)

Mapping: 2 → 6, 3 → 4
Pick from [0, 4): if we get 0→0, 1→1, 2→6, 3→4  ✓ all valid!
```

### Problem 4: Random Pick with Blacklist (LeetCode 710) [Hard]

```python
import random

class Solution:
    """
    LeetCode 710: Random Pick with Blacklist

    Idea: Map blacklisted numbers in [0, n-B) to non-blacklisted
    numbers in [n-B, n). This gives O(1) pick after O(B) init.
    """

    def __init__(self, n: int, blacklist: list[int]):
        """
        Time: O(B) where B = len(blacklist)
        Space: O(B)
        """
        self.size = n - len(blacklist)
        blacklist_set = set(blacklist)
        self.mapping = {}

        # Find non-blacklisted numbers at the tail to use as remap targets
        last = n - 1
        for b in blacklist:
            if b < self.size:
                # This blacklisted number is in our pick range — remap it
                # Find the next available non-blacklisted number from the end
                while last in blacklist_set:
                    last -= 1
                self.mapping[b] = last
                last -= 1

    def pick(self) -> int:
        """
        Time: O(1)
        """
        idx = random.randint(0, self.size - 1)
        return self.mapping.get(idx, idx)


# Usage
# n = 7, blacklist = [2, 3, 5]
# Valid picks: 0, 1, 4, 6
# sol = Solution(7, [2, 3, 5])
# sol.pick()  # Returns one of 0, 1, 4, 6 uniformly
```

---

## Complexity Analysis

| Algorithm       | Init     | Pick/Shuffle | Space | Use Case                |
| --------------- | -------- | ------------ | ----- | ----------------------- |
| Reservoir (k=1) | —        | O(n)         | O(1)  | Stream, pick 1          |
| Reservoir (k)   | —        | O(n)         | O(k)  | Stream, pick k          |
| Fisher-Yates    | —        | O(n)         | O(1)  | In-place shuffle        |
| Weighted random  | O(n)     | O(log n)     | O(n)  | Non-uniform selection   |
| Blacklist       | O(B)     | O(1)         | O(B)  | Uniform with exclusions |

---

## Common Variations

### 1. Random Pick Index (LeetCode 398) [Medium]

Pick a random index of a target value in an array with duplicates.
This is reservoir sampling applied to a filtered subset of the array.

```python
import random

class Solution:
    def __init__(self, nums: list[int]):
        self.nums = nums

    def pick(self, target: int) -> int:
        """
        Use reservoir sampling on matching elements.

        We iterate through the array, counting how many times we've
        seen the target. Each occurrence gets probability 1/count
        of being selected — classic reservoir sampling (k=1).

        Time: O(n)
        Space: O(1)
        """
        result = -1
        count = 0

        for i, num in enumerate(self.nums):
            if num == target:
                count += 1
                if random.randint(1, count) == 1:
                    result = i

        return result


# [1, 2, 3, 3, 3], target = 3
# Returns index 2, 3, or 4 with equal probability
```

### 2. Generate Random Point in a Circle (LeetCode 478) [Medium]

```python
import random
import math

class Solution:
    def __init__(self, radius: float, x_center: float, y_center: float):
        self.radius = radius
        self.x_center = x_center
        self.y_center = y_center

    def randPoint(self) -> list[float]:
        """
        Generate a uniformly random point inside a circle.

        Key insight: You can't just pick r uniformly in [0, radius]!
        If you did, points would cluster near the center because the
        area of a thin ring at radius r is proportional to r (2*pi*r*dr).

        To get uniform density, the CDF of r must match the area ratio:
          P(R <= r) = pi*r^2 / pi*R^2 = (r/R)^2
        Inverting: r = R * sqrt(uniform(0, 1))

        This "spreads out" points toward the edge, compensating for
        the larger circumference at greater radii.

        Time: O(1)
        Space: O(1)
        """
        r = math.sqrt(random.random()) * self.radius
        theta = random.random() * 2 * math.pi

        x = self.x_center + r * math.cos(theta)
        y = self.y_center + r * math.sin(theta)

        return [x, y]
```

### 3. Random Flip Matrix (LeetCode 519) [Medium]

```python
import random

class Solution:
    """
    Randomly flip 0s to 1s in a virtual m x n matrix.

    Idea: Treat the matrix as a 1D array of size m*n. Each flip() picks
    a random index from the "remaining" pool and remaps it using a
    hash map — similar to Fisher-Yates in spirit. We swap the picked
    index with the last available one (virtually) so it won't be picked again.

    Time: O(1) per flip
    Space: O(number of flips) for the mapping
    """

    def __init__(self, m: int, n: int):
        self.m = m
        self.n = n
        self.total = m * n
        self.mapping = {}  # virtual index -> actual index

    def flip(self) -> list[int]:
        # Pick a random index from [0, total - 1]
        rand_idx = random.randint(0, self.total - 1)
        self.total -= 1

        # Get the actual position (may have been remapped)
        actual = self.mapping.get(rand_idx, rand_idx)

        # Remap rand_idx to point to what's currently at the last position
        # This "removes" actual from the pool (Fisher-Yates swap logic)
        self.mapping[rand_idx] = self.mapping.get(self.total, self.total)

        # Clean up: if rand_idx == self.total, the mapping is self-referential
        # but that's fine — it just won't be accessed again

        return [actual // self.n, actual % self.n]

    def reset(self) -> None:
        """Reset all flipped cells. O(F) where F = number of flips."""
        self.total = self.m * self.n
        self.mapping.clear()
```

---

## Edge Cases

1. **Empty stream/array**: Return `None` or empty list — handle before processing
2. **k >= n (reservoir)**: Return all elements (reservoir never needs to evict)
3. **Zero or negative weights**: Invalid — they break prefix sum logic. All weights must be positive
4. **Single element**: Always return that element (both reservoir and Fisher-Yates handle this correctly)
5. **Very large streams**: Reservoir sampling shines here — O(k) memory regardless of stream size
6. **All weights equal**: Weighted selection still works but uniform random is simpler and faster
7. **Blacklist covers entire range**: `size` becomes 0 — handle by checking `self.size > 0`
8. **Floating-point weights**: Use `random.uniform(0, total)` instead of `random.randint(1, total)` for the prefix sum approach

---

## Interview Tips

1. **Know reservoir sampling by heart**: The `randint(1, i) == 1` pattern is short but easy to get wrong — practice it
2. **Walk through the probability proof**: Showing the telescoping product demonstrates deep understanding
3. **Fisher-Yates over naive shuffle**: If asked "how would you shuffle?", immediately mention Fisher-Yates and explain why naive is biased
4. **Weighted selection = prefix sum + binary search**: This pattern also appears in non-random problems
5. **Space-time tradeoffs**: Reservoir = O(k) space but O(n) per query; pre-indexing = O(n) space but O(1) per query
6. **Know when NOT to use**: If data fits in memory and size is known, `random.sample()` or `random.choice()` is simpler
7. **Rejection sampling**: An alternative for some geometric problems — generate points in a bounding box, reject those outside the target region. Simple but potentially slow if the acceptance rate is low

---

## Practice Problems

| #   | Problem                              | Difficulty | Key Concept                |
| --- | ------------------------------------ | ---------- | -------------------------- |
| 1   | LC 382: Linked List Random Node      | Medium     | Reservoir sampling (k=1)   |
| 2   | LC 384: Shuffle an Array             | Medium     | Fisher-Yates shuffle       |
| 3   | LC 528: Random Pick with Weight      | Medium     | Prefix sum + binary search |
| 4   | LC 398: Random Pick Index            | Medium     | Reservoir with filter      |
| 5   | LC 478: Random Point in Circle       | Medium     | sqrt trick for uniformity  |
| 6   | LC 519: Random Flip Matrix           | Medium     | Virtual Fisher-Yates       |
| 7   | LC 470: Implement Rand10 Using Rand7 | Medium     | Rejection sampling         |
| 8   | LC 497: Random Point in Rectangles   | Medium     | Weighted + uniform within  |
| 9   | LC 710: Random Pick with Blacklist   | Hard       | Index remapping            |

---

## Progressive Practice Problems

### Easy 1: Implement `random.choice` using only `random.random()`

Given a list, return a random element using only `random.random()` (returns float in [0, 1)).

```python
import random

def random_choice(arr: list):
    """
    Pick a uniformly random element from arr.

    random.random() returns a float in [0.0, 1.0).
    Multiply by len(arr) and floor to get a uniform index in [0, n-1].

    Time: O(1)
    Space: O(1)
    """
    if not arr:
        raise ValueError("Cannot choose from empty list")
    idx = int(random.random() * len(arr))
    return arr[idx]


# Test
counts = {}
arr = ['a', 'b', 'c', 'd']
trials = 40_000
for _ in range(trials):
    pick = random_choice(arr)
    counts[pick] = counts.get(pick, 0) + 1
for k in sorted(counts):
    print(f"{k}: {counts[k]} ({counts[k] / trials * 100:.1f}%)")
# Each should be ~25%
```

### Easy 2: Shuffle String Characters

Given a string, return a random permutation of its characters.

```python
import random

def shuffle_string(s: str) -> str:
    """
    Return a uniformly random permutation of the input string.

    Convert to list (strings are immutable), apply Fisher-Yates, join back.

    Time: O(n)
    Space: O(n) — for the character list
    """
    chars = list(s)
    for i in range(len(chars) - 1, 0, -1):
        j = random.randint(0, i)
        chars[i], chars[j] = chars[j], chars[i]
    return ''.join(chars)


# Test
print(shuffle_string("abcdef"))  # e.g., "dbafce"
```

### Medium 1: Random Subset of Size k (without replacement)

Select k random elements from an array of size n, each subset equally likely.
This is Fisher-Yates stopped early — only shuffle k positions.

```python
import random

def random_subset(arr: list, k: int) -> list:
    """
    Return k distinct random elements from arr (all subsets equally likely).

    Optimization: Run Fisher-Yates for only k steps instead of n.
    After k swaps, the last k elements form a uniformly random subset.

    Time: O(k) — not O(n)!
    Space: O(1) — modifies arr in-place (pass a copy if needed)
    """
    n = len(arr)
    k = min(k, n)  # Handle k > n gracefully

    for i in range(n - 1, n - 1 - k, -1):
        j = random.randint(0, i)
        arr[i], arr[j] = arr[j], arr[i]

    return arr[n - k:]


# Test
nums = list(range(1, 11))  # [1, 2, ..., 10]
print(random_subset(nums[:], 3))  # e.g., [7, 2, 9]
```

### Medium 2: Implement Rand10 Using Rand7 (LeetCode 470)

Given a function `rand7()` that returns a uniform random integer in `[1, 7]`,
implement `rand10()` that returns a uniform random integer in `[1, 10]`.

**Approach:** Use rejection sampling. Call `rand7()` twice to generate a number
in [1, 49] uniformly. If it's in [1, 40], return `(value - 1) % 10 + 1`.
Otherwise, reject and retry. Expected calls to rand7: ~2.45 per rand10 call.

```python
import random

def rand7() -> int:
    """Simulates the given rand7() API."""
    return random.randint(1, 7)

def rand10() -> int:
    """
    Generate uniform random int in [1, 10] using only rand7().

    Key idea: rand7() gives 7 outcomes. Two calls give 7*7 = 49
    equally likely outcomes. Map [1, 40] to [1, 10] (4 outcomes each),
    reject [41, 49] and retry.

    Time: O(1) expected (rejection probability = 9/49 ≈ 18%)
    Space: O(1)
    """
    while True:
        # Generate uniform random in [1, 49]
        row = rand7()          # 1-7
        col = rand7()          # 1-7
        idx = (row - 1) * 7 + col  # 1-49, uniformly distributed

        if idx <= 40:
            return (idx - 1) % 10 + 1  # Map to [1, 10]
        # else: reject and retry (probability 9/49)


# Test
counts = {}
trials = 100_000
for _ in range(trials):
    val = rand10()
    counts[val] = counts.get(val, 0) + 1
for k in sorted(counts):
    print(f"{k}: {counts[k]} ({counts[k] / trials * 100:.1f}%)")
# Each should be ~10%
```

### Medium 3: Random Point in Non-Overlapping Rectangles (LeetCode 497)

Given a list of non-overlapping axis-aligned rectangles, pick a random integer
coordinate point uniformly across all rectangles.

**Approach:** Each rectangle has `(x2-x1+1) * (y2-y1+1)` integer points. Use
weighted random selection (by area) to pick a rectangle, then pick a uniform
point within it.

```python
import random
import bisect

class Solution:
    def __init__(self, rects: list[list[int]]):
        """
        Build prefix sums of rectangle areas (number of integer points).

        Time: O(n)
        Space: O(n)
        """
        self.rects = rects
        self.prefix = []
        running = 0
        for x1, y1, x2, y2 in rects:
            # Number of integer points in this rectangle
            area = (x2 - x1 + 1) * (y2 - y1 + 1)
            running += area
            self.prefix.append(running)
        self.total = running

    def pick(self) -> list[int]:
        """
        1. Weighted random pick of a rectangle (proportional to area)
        2. Uniform random point within that rectangle

        Time: O(log n)
        Space: O(1)
        """
        target = random.randint(1, self.total)
        rect_idx = bisect.bisect_left(self.prefix, target)

        x1, y1, x2, y2 = self.rects[rect_idx]
        x = random.randint(x1, x2)
        y = random.randint(y1, y2)
        return [x, y]


# Usage
# rects = [[-2, -2, -1, -1], [1, 0, 3, 0]]
# sol = Solution(rects)
# sol.pick()  # Random integer point from either rectangle
```

### Medium 4: Weighted Random with Updates (Segment Tree Approach)

When weights change frequently, prefix sums require O(n) to rebuild.
A **segment tree** supports both update and query in O(log n).

```python
import random

class DynamicWeightedRandom:
    """
    Weighted random selection with O(log n) updates.

    Uses a segment tree where each node stores the sum of weights
    in its subtree. To pick, descend the tree using a random target.

    The tree is padded to the next power of 2 so the implicit
    binary tree structure works correctly for all sizes.

    Init: O(n)
    Pick: O(log n)
    Update: O(log n)
    Space: O(n)
    """

    def __init__(self, weights: list[int]):
        # Pad to next power of 2 for correct tree structure
        self.n = 1
        while self.n < len(weights):
            self.n *= 2

        self.tree = [0] * (2 * self.n)
        # Place weights in leaf nodes (index n..n+len(weights)-1)
        for i, w in enumerate(weights):
            self.tree[self.n + i] = w
        # Build internal nodes bottom-up
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]

    def update(self, index: int, new_weight: int) -> None:
        """Update weight at index in O(log n)."""
        pos = self.n + index
        self.tree[pos] = new_weight
        pos //= 2
        while pos >= 1:
            self.tree[pos] = self.tree[2 * pos] + self.tree[2 * pos + 1]
            pos //= 2

    def pick(self) -> int:
        """Pick random index proportional to weight in O(log n)."""
        if self.tree[1] == 0:
            raise ValueError("All weights are zero")
        target = random.randint(1, self.tree[1])  # tree[1] = total weight
        node = 1
        while node < self.n:
            left_sum = self.tree[2 * node]
            if target <= left_sum:
                node = 2 * node       # Go left
            else:
                target -= left_sum
                node = 2 * node + 1   # Go right
        return node - self.n


# Test
dwr = DynamicWeightedRandom([1, 3, 2])
counts = {0: 0, 1: 0, 2: 0}
for _ in range(60000):
    counts[dwr.pick()] += 1
print("Before update:", counts)  # ~{0: 10000, 1: 30000, 2: 20000}

dwr.update(1, 1)  # Change weight of index 1 from 3 to 1
counts = {0: 0, 1: 0, 2: 0}
for _ in range(40000):
    counts[dwr.pick()] += 1
print("After update:", counts)   # ~{0: 10000, 1: 10000, 2: 20000}
```

### Hard 1: Sampling from a Weighted Stream (Weighted Reservoir Sampling)

Extend reservoir sampling to a weighted stream where item `i` has weight `w_i`.
Each item should appear in the final sample with probability proportional to its weight.

```python
import random
import heapq

def weighted_reservoir_sample(stream, k: int) -> list:
    """
    Weighted reservoir sampling (Efraimidis-Spirakis algorithm).

    For each item, compute a key = random() ^ (1/weight). Keep
    the k items with the largest keys. Items with higher weights
    generate higher keys on average, so they're more likely to stay.

    Why it works: For item with weight w, key = U^(1/w) where U ~ Uniform(0,1).
    The CDF of this key is P(U^(1/w) <= x) = P(U <= x^w) = x^w.
    Higher weight → the CDF grows faster → higher keys on average.

    Time: O(n log k) with a heap
    Space: O(k)
    """
    reservoir = []  # min-heap of (key, tiebreaker, item)

    for idx, (item, weight) in enumerate(stream):
        if weight <= 0:
            continue  # Skip non-positive weights

        # key = uniform(0,1) ^ (1/w) — higher weight → higher key on average
        key = random.random() ** (1.0 / weight)

        if len(reservoir) < k:
            # Use idx as tiebreaker to avoid comparing items directly
            heapq.heappush(reservoir, (key, idx, item))
        elif key > reservoir[0][0]:
            heapq.heapreplace(reservoir, (key, idx, item))

    return [item for _, _, item in reservoir]


# Test: item 'B' (weight 5) should appear ~5x as often as 'A' (weight 1)
stream_data = [('A', 1), ('B', 5), ('C', 2), ('D', 1), ('E', 1)]
counts = {}
for _ in range(100_000):
    sample = weighted_reservoir_sample(iter(stream_data), 1)
    for item in sample:
        counts[item] = counts.get(item, 0) + 1
total = sum(counts.values())
for k in sorted(counts):
    print(f"{k}: {counts[k] / total:.3f}")
# Expected roughly: A: 0.1, B: 0.5, C: 0.2, D: 0.1, E: 0.1
```

### Hard 2: Online Random Sampling with Removal

Design a data structure that supports: insert(val), remove(val), and getRandom() — all in O(1).
This is LeetCode 380: Insert Delete GetRandom O(1).

**Key Insight:** Use an array for O(1) random access and a hash map for O(1) lookup.
For O(1) removal, swap the element to remove with the last element, then pop.

```python
import random

class RandomizedSet:
    """
    LeetCode 380: Insert Delete GetRandom O(1)

    Maintain an array for random access and a hash map {val -> index}
    for O(1) lookup. On removal, swap with last element to avoid
    shifting the array.

    All operations: O(1) average
    Space: O(n)
    """

    def __init__(self):
        self.vals = []            # Dynamic array of values
        self.val_to_idx = {}      # val -> index in self.vals

    def insert(self, val: int) -> bool:
        """Insert val. Return True if val was not already present."""
        if val in self.val_to_idx:
            return False
        self.val_to_idx[val] = len(self.vals)
        self.vals.append(val)
        return True

    def remove(self, val: int) -> bool:
        """Remove val. Return True if val was present."""
        if val not in self.val_to_idx:
            return False

        # Swap val with the last element
        idx = self.val_to_idx[val]
        last_val = self.vals[-1]

        self.vals[idx] = last_val
        self.val_to_idx[last_val] = idx

        # Remove the last element (which is now val)
        self.vals.pop()
        del self.val_to_idx[val]
        return True

    def getRandom(self) -> int:
        """Return a random element from the set."""
        return random.choice(self.vals)


# Usage
# rs = RandomizedSet()
# rs.insert(1)    # True
# rs.insert(2)    # True
# rs.remove(1)    # True
# rs.insert(2)    # False (already exists)
# rs.getRandom()  # Returns 2 (only element)
```

### Hard 3: Insert Delete GetRandom O(1) — Duplicates Allowed (LeetCode 381)

Extension of the above where duplicates are allowed. Each element should have
equal probability regardless of how many copies exist.

```python
import random

class RandomizedCollection:
    """
    LeetCode 381: Insert Delete GetRandom O(1) - Duplicates allowed.

    Similar to LC 380, but val_to_indices maps each value to a SET
    of indices (since duplicates exist). On removal, we still swap
    with the last element.

    All operations: O(1) average
    Space: O(n)
    """

    def __init__(self):
        self.vals = []
        self.val_to_indices = {}  # val -> set of indices

    def insert(self, val: int) -> bool:
        """Insert val. Return True if val was not already present."""
        not_present = val not in self.val_to_indices or len(self.val_to_indices[val]) == 0

        if val not in self.val_to_indices:
            self.val_to_indices[val] = set()
        self.val_to_indices[val].add(len(self.vals))
        self.vals.append(val)
        return not_present

    def remove(self, val: int) -> bool:
        """Remove one copy of val. Return True if val was present."""
        if val not in self.val_to_indices or len(self.val_to_indices[val]) == 0:
            return False

        # Get an arbitrary index of val
        idx = self.val_to_indices[val].pop()
        last_val = self.vals[-1]
        last_idx = len(self.vals) - 1

        if idx != last_idx:
            # Swap val at idx with the last element
            self.vals[idx] = last_val
            self.val_to_indices[last_val].discard(last_idx)
            self.val_to_indices[last_val].add(idx)

        self.vals.pop()
        # If we popped val from the end but idx == last_idx, we already
        # removed it from val_to_indices via .pop() above.
        # If idx != last_idx, the swap already handled it.

        # Clean up empty sets
        if len(self.val_to_indices[val]) == 0:
            del self.val_to_indices[val]

        return True

    def getRandom(self) -> int:
        """Return a random element. Each element has equal probability."""
        return random.choice(self.vals)


# Usage
# rc = RandomizedCollection()
# rc.insert(1)    # True
# rc.insert(1)    # False (duplicate)
# rc.insert(2)    # True
# rc.getRandom()  # 2/3 chance of 1, 1/3 chance of 2
# rc.remove(1)    # True
# rc.getRandom()  # 1/2 chance of 1, 1/2 chance of 2
```

---

## When NOT to Use These Algorithms

### When NOT to use Reservoir Sampling

1. **Data fits in memory**: Just store it all and pick randomly
2. **You can make multiple passes**: Easier approaches exist
3. **Stream is small and known size**: Simple `random.sample()` works

### When NOT to use Fisher-Yates

1. **Only need one random element**: Just use `random.choice()`
2. **Need the array unchanged**: Fisher-Yates is in-place; copy first if needed
3. **Built-in exists**: `random.shuffle()` in Python is already Fisher-Yates

### When NOT to use Weighted Random

1. **Equal weights**: Use uniform random selection
2. **Weights change frequently**: Rebuilding prefix sums is O(n) per change — use a segment tree instead
3. **Single selection**: Building the structure is overkill — just pick a random number in [0, total_weight] and iterate through weights

> **Common mistake**: Using naive shuffle `for i: swap with random j in [0, n)` — this
> generates `n^n` outcomes mapped to `n!` permutations, causing bias. Always use Fisher-Yates.

---

## Related Sections

- [Binary Search](../10-binary-search/README.md) - Used in weighted random
- [Prefix Sums](../02-arrays-strings/06-prefix-sum.md) - Foundation for weighted selection
