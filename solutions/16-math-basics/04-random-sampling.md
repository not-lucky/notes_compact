# Practice Problems: Random Sampling

This file contains optimal Python solutions for the practice problems listed in the Random Sampling notes.

---

## 1. Linked List Random Node

**Problem Statement:**
Given a singly linked list, return a random node's value from the linked list. Each node must have the same probability of being chosen.

**Examples & Edge Cases:**

- **Example:** `head = [1, 2, 3]`. `getRandom()` should return 1, 2, or 3 with $P=1/3$.
- **Edge Case:** Single node list.
- **Edge Case:** Extremely long list where you cannot store all values in memory (requires Reservoir Sampling).

**Optimal Python Solution:**

```python
import random

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def __init__(self, head: ListNode):
        """
        Initializes the object with the head of the singly-linked list.
        """
        self.head = head

    def getRandom(self) -> int:
        """
        Returns a random node's value using Reservoir Sampling.
        """
        # Start with the first node's value
        result = self.head.val
        curr = self.head.next

        # Track the number of nodes seen so far
        n = 2
        while curr:
            # For the i-th node, replace the current result with
            # probability 1/i.
            if random.random() < (1 / n):
                result = curr.val
            curr = curr.next
            n += 1

        return result
```

**Explanation:**

1. **Reservoir Sampling**: Since we don't know the length of the list beforehand (or if it's a stream), we use reservoir sampling.
2. **Probability Logic**:
   - We keep the first element.
   - For the 2nd element, we pick it with probability 1/2.
   - For the 3rd element, we pick it with probability 1/3.
   - In general, for the $i$-th element, we replace the currently selected element with probability $1/i$.
3. **Fairness**: Mathematically, after $N$ elements, each element has exactly $1/N$ probability of being the final selection.

**Complexity Analysis:**

- **Time Complexity:** $O(N)$ for each call to `getRandom()`, where $N$ is the number of nodes in the linked list.
- **Space Complexity:** $O(1)$ as we only store the current selection and a counter.

---

## 2. Shuffle an Array

**Problem Statement:**
Given an integer array `nums`, design an algorithm to randomly shuffle the array. All permutations of the array should be equally likely as a result of the shuffling.

**Examples & Edge Cases:**

- **Example:** `nums = [1, 2, 3]`. `shuffle()` could return `[3, 1, 2]`, `[2, 3, 1]`, etc.
- **Edge Case:** Empty array or single element array.

**Optimal Python Solution:**

```python
import random

class Solution:
    def __init__(self, nums: list[int]):
        self.original = list(nums)
        self.nums = nums

    def reset(self) -> list[int]:
        """
        Resets the array to its original configuration and returns it.
        """
        self.nums = list(self.original)
        return self.nums

    def shuffle(self) -> list[int]:
        """
        Returns a random shuffling of the array using Fisher-Yates algorithm.
        """
        # Fisher-Yates Shuffle
        for i in range(len(self.nums) - 1, 0, -1):
            # Pick a random index from 0 to i
            j = random.randint(0, i)
            # Swap elements at i and j
            self.nums[i], self.nums[j] = self.nums[j], self.nums[i]

        return self.nums
```

**Explanation:**

1. **Fisher-Yates Algorithm**: To shuffle an array of $n$ elements, we iterate through the array from last to first.
2. **Uniform Selection**: At each index $i$, we pick a random index $j$ such that $0 \le j \le i$ and swap elements at $i$ and $j$.
3. **Correctness**: This algorithm ensures that each of the $n!$ permutations is equally likely. A common mistake is picking $j$ from $0$ to $n-1$ every time, which introduces bias.

**Complexity Analysis:**

- **Time Complexity:** $O(N)$ per shuffle call.
- **Space Complexity:** $O(N)$ to store the original configuration for the `reset` functionality.

---

## 3. Random Pick with Weight

**Problem Statement:**
You are given a 0-indexed array of positive integers `w` where `w[i]` describes the weight of the $i$-th index. You need to implement the function `pickIndex()`, which randomly picks an index in the range $[0, w.length - 1]$ and returns it. The probability of picking an index $i$ is $w[i] / \text{sum}(w)$.

**Examples & Edge Cases:**

- **Example:** `w = [1, 3]`. Index 0 should be picked with $1/4$ probability, Index 1 with $3/4$ probability.
- **Edge Case:** Weights are all the same -> Equal probability.
- **Edge Case:** Single weight.

**Optimal Python Solution:**

```python
import random
import bisect

class Solution:
    def __init__(self, w: list[int]):
        self.prefix_sums = []
        current_sum = 0
        for weight in w:
            current_sum += weight
            self.prefix_sums.append(current_sum)
        self.total_sum = current_sum

    def pickIndex(self) -> int:
        """
        Picks an index based on weights using Prefix Sum and Binary Search.
        """
        # Pick a random number in range [1, total_sum]
        target = random.randint(1, self.total_sum)

        # Find the first prefix sum >= target using binary search
        # bisect_left returns the leftmost insertion point
        return bisect.bisect_left(self.prefix_sums, target)
```

**Explanation:**

1. **Mapping to a Range**: If weights are `[1, 3]`, the prefix sums are `[1, 4]`. This maps index 0 to range $[1, 1]$ and index 1 to range $[2, 4]$.
2. **Binary Search**: Once we pick a random number in the total range, we use binary search on the sorted `prefix_sums` to find which "bucket" the number falls into. This is significantly faster than a linear scan for large number of weights.

**Complexity Analysis:**

- **Time Complexity:**
  - Constructor: $O(N)$ to compute prefix sums.
  - `pickIndex`: $O(\log N)$ due to binary search.
- **Space Complexity:** $O(N)$ to store the prefix sums.

---

## 4. Random Pick Index

**Problem Statement:**
Given an integer array `nums` with possible duplicates, randomly output the index of a given `target` number. You can assume that the given target number must exist in the array. Each index should have the same probability of being returned.

**Examples & Edge Cases:**

- **Example:** `nums = [1, 2, 3, 3, 3], target = 3`. Return 2, 3, or 4 with $P=1/3$.
- **Edge Case:** Target appears only once.
- **Edge Case:** Memory constraints (if `nums` is too large to pre-process).

**Optimal Python Solution:**

```python
import random

class Solution:
    def __init__(self, nums: list[int]):
        self.nums = nums

    def pick(self, target: int) -> int:
        """
        Returns a random index of target using Reservoir Sampling.
        """
        count = 0
        res = -1

        for i, num in enumerate(self.nums):
            if num == target:
                count += 1
                # If we've seen 'count' occurrences of target,
                # the probability of picking the current index is 1/count.
                if random.randint(1, count) == 1:
                    res = i
        return res
```

**Explanation:**

1. **Reservoir Sampling on target**: Instead of sampling from all elements, we only sample from elements that match the target.
2. **Logic**: The first time we see the target, we pick its index with $P=1/1$. The second time, we replace it with $P=1/2$, and so on.
3. **Advantage**: This approach uses $O(1)$ extra space (excluding the input array), which is useful if the array is accessed as a stream.

**Complexity Analysis:**

- **Time Complexity:** $O(N)$ per `pick` call.
- **Space Complexity:** $O(1)$ additional space.

---

## 5. Random Pick with Blacklist

**Problem Statement:**
Given an integer `n` and an array of unique integers `blacklist`, design an algorithm to pick a random integer in the range $[0, n - 1]$ that is NOT in the `blacklist`. Any integer not in the blacklist should be equally likely to be returned.

**Examples & Edge Cases:**

- **Example:** `n = 7, blacklist = [2, 3, 5]`. Valid picks are `0, 1, 4, 6`.
- **Edge Case:** Blacklist is empty.
- **Edge Case:** `n` is very large ($10^9$) but blacklist is small ($10^5$).

**Optimal Python Solution:**

```python
import random

class Solution:
    def __init__(self, n: int, blacklist: list[int]):
        # The number of valid integers is n - len(blacklist)
        self.valid_count = n - len(blacklist)
        self.mapping = {}

        # We want to map blacklisted numbers in the range [0, valid_count - 1]
        # to non-blacklisted numbers in the range [valid_count, n - 1].
        blacklist_set = set(blacklist)

        # Potential replacements start from the end of the range
        last = n - 1

        # Only blacklisted numbers in the [0, valid_count-1] range need remapping
        for b in blacklist:
            if b < self.valid_count:
                # Find the next available non-blacklisted number at the end
                while last in blacklist_set:
                    last -= 1
                self.mapping[b] = last
                last -= 1

    def pick(self) -> int:
        """
        Returns a random non-blacklisted integer in O(1).
        """
        idx = random.randint(0, self.valid_count - 1)
        # If the chosen index is blacklisted, return its remapped value
        return self.mapping.get(idx, idx)
```

**Explanation:**

1. **Virtual Array**: Imagine an array of all valid numbers. Its size is `n - len(blacklist)`.
2. **Remapping**: We pick a random number `idx` from `[0, valid_count - 1]`. If `idx` is in the blacklist, it's like that slot is "broken". We "repair" it by mapping that `idx` to a valid number that exists in the upper part of the range `[valid_count, n - 1]`.
3. **Efficiency**: By using a hash map for remapping, `pick()` becomes $O(1)$.

**Complexity Analysis:**

- **Time Complexity:**
  - Constructor: $O(B)$ where $B$ is the size of the blacklist.
  - `pick`: $O(1)$.
- **Space Complexity:** $O(B)$ to store the mapping for blacklisted numbers.

---

## 6. Generate Random Point in Circle

**Problem Statement:**
Given the radius and the $x, y$ coordinates of the center of a circle, generate a uniform random point inside the circle.

**Examples & Edge Cases:**

- **Example:** `radius = 1.0, x_center = 0, y_center = 0`.
- **Edge Case:** Radius is 0.
- **Mathematical Trap:** Picking `radius` and `theta` uniformly leads to points clustering at the center.

**Optimal Python Solution:**

```python
import random
import math

class Solution:
    def __init__(self, radius: float, x_center: float, y_center: float):
        self.radius = radius
        self.x = x_center
        self.y = y_center

    def randPoint(self) -> list[float]:
        """
        Generates a uniform random point using the Square Root trick.
        """
        # Uniformly pick theta in [0, 2*pi]
        theta = random.uniform(0, 2 * math.pi)

        # Uniformly pick r^2, so r = sqrt(uniform(0, 1)) * radius
        # This accounts for the fact that area increases with r^2
        r = math.sqrt(random.uniform(0, 1)) * self.radius

        return [self.x + r * math.cos(theta), self.y + r * math.sin(theta)]
```

**Explanation:**

1. **Area Bias**: In polar coordinates, the area of a thin ring is $2\pi r \cdot dr$. Because the area increases as we move further from the center, picking $r$ uniformly would result in higher density at the center.
2. **Correction**: The cumulative distribution function (CDF) for the radius in a uniform circle is $F(r) = (r/R)^2$. To sample from this, we take the inverse: $r = R \sqrt{U}$, where $U$ is a uniform random variable in $[0, 1]$.
3. **Alternative**: Rejection sampling (picking a point in a bounding box and checking if it's in the circle) is also valid but may take multiple attempts.

**Complexity Analysis:**

- **Time Complexity:** $O(1)$.
- **Space Complexity:** $O(1)$.
