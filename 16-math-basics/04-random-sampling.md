# Random Sampling

> **Prerequisites:** None (standalone topic)

## Building Intuition

**The "Fair Lottery" Mental Model**

Imagine you're running a lottery where people buy tickets as they arrive, but you don't know how many will show up:
- You can only hold k winning tickets in your hand
- You must be fair—everyone has equal chance of winning
- You can't go back to earlier tickets

Reservoir sampling solves this: keep k items, and as new ones arrive, randomly decide whether to swap.

**Why the Math Works**

For selecting 1 item from n:
- Keep first item with probability 1
- On item i, replace with probability 1/i

After n items, probability any item is kept:
```
P(item k is final) = P(picked at k) × P(survived all later rounds)
                   = (1/k) × (k/(k+1)) × ((k+1)/(k+2)) × ... × ((n-1)/n)
                   = 1/n ✓
```

Each item has exactly 1/n chance—perfectly fair!

**Fisher-Yates: The Perfect Shuffle**

A biased shuffle: `for i, pick random j, swap` gives some permutations higher probability.
Fisher-Yates: `for i from n-1 to 1, pick j from 0 to i, swap` is provably uniform.

The key difference is shrinking the random range as you go.

---

## Interview Context

Random sampling algorithms appear when:
- Selecting random elements from a stream of unknown size
- Shuffling arrays fairly
- Generating random permutations
- Weighted random selection
- Monte Carlo algorithms

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

i=1: result = 5       (always keep first)
i=2: rand(2) = 0 → keep 5, or 1 → replace with 2
     Say we get 1, result = 2
i=3: rand(3) = 0,1,2  (replace if 0)
     Say we get 2, result = 2 (keep)
i=4: rand(4) = 0,1,2,3 (replace if 0)
     Say we get 0, result = 1
i=5: rand(5) = 0,1,2,3,4 (replace if 0)
     Say we get 3, result = 1 (keep)
i=6: rand(6) = 0,1,2,3,4,5 (replace if 0)
     Say we get 5, result = 1 (keep)

Final: 1 (each of 6 elements had 1/6 chance)
```

---

## Implementation

### Reservoir Sampling: Pick 1 Random Element

```python
import random

def reservoir_sample_one(stream) -> any:
    """
    Select one random element from a stream using O(1) space.

    Each element has equal probability 1/n of being selected.

    Time: O(n) - single pass
    Space: O(1)
    """
    result = None

    for i, item in enumerate(stream, 1):  # 1-indexed
        # With probability 1/i, replace result with current item
        if random.randint(1, i) == 1:
            result = item

    return result


# Test
stream = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
counts = {}
for _ in range(100000):
    result = reservoir_sample_one(iter(stream))
    counts[result] = counts.get(result, 0) + 1

# Each should be ~10000 (10% of trials)
for k in sorted(counts):
    print(f"{k}: {counts[k]} ({counts[k]/1000:.1f}%)")
```

### Reservoir Sampling: Pick k Random Elements

```python
import random

def reservoir_sample_k(stream, k: int) -> list:
    """
    Select k random elements from a stream using O(k) space.

    Time: O(n)
    Space: O(k)
    """
    reservoir = []

    for i, item in enumerate(stream):
        if i < k:
            # Fill reservoir initially
            reservoir.append(item)
        else:
            # Replace element with probability k/(i+1)
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

## Problem: Linked List Random Node (LeetCode 382)

Given a singly linked list, return a random node's value with equal probability.

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
        Return a random node value using reservoir sampling.

        Time: O(n)
        Space: O(1)
        """
        result = self.head.val
        node = self.head.next
        i = 2

        while node:
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
For position n-1: We choose from n elements → 1/n for each
For position n-2: We choose from n-1 remaining → 1/(n-1) for each
...
For position 0: Only 1 element left

Total permutations: n × (n-1) × ... × 1 = n!
Each is equally likely.
```

---

## Implementation

### Fisher-Yates Shuffle (In-Place)

```python
import random

def shuffle(arr: list) -> list:
    """
    Shuffle array in-place using Fisher-Yates algorithm.

    Time: O(n)
    Space: O(1)
    """
    n = len(arr)
    for i in range(n - 1, 0, -1):
        j = random.randint(0, i)
        arr[i], arr[j] = arr[j], arr[i]
    return arr


# Test
arr = [1, 2, 3, 4, 5]
print(shuffle(arr))  # Random permutation
```

### Shuffle Array Problem (LeetCode 384)

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
        """Return a random shuffling of the array."""
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

Select an element where each has a different probability.

### Using Prefix Sums

```python
import random
import bisect

class WeightedRandom:
    """
    Select elements with probability proportional to their weights.

    Example: weights = [1, 3, 2]
    Total = 6
    P(index 0) = 1/6
    P(index 1) = 3/6 = 1/2
    P(index 2) = 2/6 = 1/3
    """

    def __init__(self, weights: list[int]):
        """
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

        Time: O(log n) - binary search
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

## Problem: Random Pick with Weight (LeetCode 528)

```python
import random
import bisect

class Solution:
    def __init__(self, w: list[int]):
        self.prefix = []
        running = 0
        for weight in w:
            running += weight
            self.prefix.append(running)
        self.total = running

    def pickIndex(self) -> int:
        target = random.randint(1, self.total)
        return bisect.bisect_left(self.prefix, target)


# Usage
# weights = [1, 3]
# sol = Solution(weights)
# Over many calls, pickIndex() returns 0 about 1/4 of the time, 1 about 3/4
```

---

## Pattern: Random Pick with Blacklist

Select uniformly from `[0, n)` excluding a blacklist.

```python
import random

class Solution:
    """
    LeetCode 710: Random Pick with Blacklist

    Idea: Map blacklisted numbers to non-blacklisted numbers at the end.
    """

    def __init__(self, n: int, blacklist: list[int]):
        """
        Time: O(B) where B = len(blacklist)
        Space: O(B)
        """
        self.size = n - len(blacklist)
        blacklist_set = set(blacklist)
        self.mapping = {}

        # Numbers at the end that are not blacklisted
        last = n - 1
        for b in blacklist:
            if b < self.size:
                # Need to remap this blacklisted number
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

| Algorithm | Time | Space | Use Case |
|-----------|------|-------|----------|
| Reservoir (k=1) | O(n) | O(1) | Stream, pick 1 |
| Reservoir (k) | O(n) | O(k) | Stream, pick k |
| Fisher-Yates | O(n) | O(1) | In-place shuffle |
| Weighted random | O(log n) pick | O(n) | Non-uniform selection |

---

## Common Variations

### 1. Random Pick Index (LeetCode 398)

Pick a random index of a target value in an array with duplicates.

```python
import random

class Solution:
    def __init__(self, nums: list[int]):
        self.nums = nums

    def pick(self, target: int) -> int:
        """Use reservoir sampling on matching elements."""
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

### 2. Generate Random Point in a Circle

```python
import random
import math

def random_point_in_circle(radius: float, x_center: float, y_center: float) -> list[float]:
    """
    Generate uniformly random point inside a circle.

    Key insight: Can't just pick (r, theta) uniformly!
    Area grows with r², so we need r = sqrt(uniform(0, 1)) × radius
    """
    # Use rejection sampling or the sqrt trick
    r = math.sqrt(random.random()) * radius
    theta = random.random() * 2 * math.pi

    x = x_center + r * math.cos(theta)
    y = y_center + r * math.sin(theta)

    return [x, y]
```

### 3. Random Flip Matrix (LeetCode 519)

```python
import random

class Solution:
    """Randomly flip 0s to 1s in a matrix."""

    def __init__(self, m: int, n: int):
        self.m = m
        self.n = n
        self.total = m * n
        self.mapping = {}

    def flip(self) -> list[int]:
        # Pick random from remaining
        idx = random.randint(0, self.total - 1)
        self.total -= 1

        # Get actual position (may be remapped)
        result = self.mapping.get(idx, idx)

        # Map idx to the last available position
        self.mapping[idx] = self.mapping.get(self.total, self.total)

        return [result // self.n, result % self.n]

    def reset(self) -> None:
        self.total = self.m * self.n
        self.mapping.clear()
```

---

## Edge Cases

1. **Empty stream**: Return None or handle gracefully
2. **k > n**: Return all elements
3. **Zero weights**: Skip or handle as error
4. **Single element**: Always return that element
5. **Very large streams**: Reservoir sampling is designed for this

---

## Interview Tips

1. **Know reservoir sampling by heart**: It's elegant and impressive
2. **Explain the probability math**: Shows deep understanding
3. **Fisher-Yates over naive shuffle**: Naive `random.choice` for each position is biased
4. **Weighted → prefix sum + binary search**: Common pattern
5. **Mention space-time tradeoffs**: Reservoir = O(k) space, pre-indexing = O(n) space

---

## Practice Problems

| # | Problem | Difficulty | Key Concept |
|---|---------|------------|-------------|
| 1 | Linked List Random Node | Medium | Reservoir sampling |
| 2 | Shuffle an Array | Medium | Fisher-Yates shuffle |
| 3 | Random Pick with Weight | Medium | Prefix sum + binary search |
| 4 | Random Pick Index | Medium | Reservoir with filter |
| 5 | Random Pick with Blacklist | Hard | Remapping |
| 6 | Generate Random Point in Circle | Medium | Rejection or sqrt trick |

---

## When NOT to Use These Algorithms

### When NOT to use Reservoir Sampling
1. **Data fits in memory**: Just store it all and pick randomly
2. **You can make multiple passes**: Easier approaches exist
3. **Stream is small and known size**: Simple `random.sample()` works

### When NOT to use Fisher-Yates
1. **Only need one random element**: Just use `random.choice()`
2. **Need partial shuffle**: Shuffle only what you need
3. **Built-in exists**: `random.shuffle()` in Python is already Fisher-Yates

### When NOT to use Weighted Random
1. **Equal weights**: Use uniform random selection
2. **Weights change frequently**: Rebuilding prefix sums is O(n)
3. **Single selection**: Building the structure is overkill

**Common mistake**: Using naive shuffle `for i: swap with random j in [0,n)` which is biased.

---

## Related Sections

- [Binary Search](../10-binary-search/README.md) - Used in weighted random
- [Prefix Sums](../02-arrays-strings/06-prefix-sum.md) - Foundation for weighted selection
