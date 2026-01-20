# Monotonic Queue / Sliding Window Maximum

> **Prerequisites:** [02-queue-basics](./02-queue-basics.md), [04-monotonic-stack](./04-monotonic-stack.md)

## Overview

A monotonic queue (or monotonic deque) is a double-ended queue that maintains elements in sorted order while also supporting efficient removal of expired elements. It combines the monotonic property of monotonic stacks with the sliding window capability of queues, making it perfect for problems like "maximum/minimum in every sliding window."

## Building Intuition

**Why does a monotonic deque solve sliding window max/min?**

The key insight is recognizing which elements can never be the answer:

1. **Dominance principle**: In a window, if element A comes before element B and A ≤ B, then A can never be the maximum of any window containing B. Why? Because any window containing A also contains B (since B comes after A), and B ≥ A.

2. **Expiration principle**: Elements outside the current window are irrelevant. We need to efficiently remove them.

**The Core Insight**:
```
An element is only useful if:
1. It might be the maximum (no larger element to its right in the window)
2. It's still in the current window

We can maintain exactly these "useful" elements in a monotonic deque.
```

**Worked Example - Sliding Window Maximum (k=3)**:
```
Array: [1, 3, -1, -3, 5, 3, 6, 7]

i=0: push 0          deque: [0]       (values: [1])
i=1: 3 > 1, pop 0    deque: []
     push 1          deque: [1]       (values: [3])
i=2: -1 < 3, push 2  deque: [1,2]     (values: [3,-1])
     Window [0,1,2], max = deque[0] = 3

i=3: -3 < -1, push 3 deque: [1,2,3]   (values: [3,-1,-3])
     Check: 1 >= 3-3+1=1 ✓ (index 1 still in window)
     Window [1,2,3], max = 3

i=4: 5 > -3, pop 3   deque: [1,2]
     5 > -1, pop 2   deque: [1]
     5 > 3, pop 1    deque: []
     push 4          deque: [4]       (values: [5])
     Window [2,3,4], max = 5

...and so on
```

**Why We Need a Deque (Not Just Stack)**:
- **Pop from back**: Remove elements smaller than the new element (maintaining monotonic property)
- **Pop from front**: Remove elements outside the window (maintaining window constraint)
- A stack only allows pop from one end, but we need both!

**Mental Model**: Imagine a "hall of champions" where only potential winners stay. When a new contender arrives:
1. Anyone weaker (to the right of the door) is kicked out—they'll never win
2. Anyone whose time has passed (too old) leaves through the other door
3. The current champion (front) is the window maximum

## When NOT to Use Monotonic Deques

Monotonic deques are the wrong choice when:

1. **No Fixed Window Size**: If the window size varies or there's no sliding window concept, consider segment trees or other structures.

2. **Need Both Max AND Min**: A single monotonic deque tracks one extreme. For both, you need two deques (one increasing, one decreasing).

3. **Window Contains Complex Objects**: If comparison is expensive or objects have multiple sortable dimensions, other approaches may be simpler.

4. **Updates Within Window**: If you need to update values inside the window (not just add/remove at ends), monotonic deques don't support this—use segment trees.

5. **Non-Contiguous Windows**: Monotonic deques assume contiguous sliding windows. For windows with gaps or jumps, different techniques are needed.

**Alternative Approaches**:
| Scenario | Better Approach |
|----------|-----------------|
| No fixed window | Segment tree |
| Both max and min | Two monotonic deques |
| Updates in window | Balanced BST or segment tree |
| One-time query | Linear scan or heap |

## Interview Context

The sliding window maximum problem is a **classic hard problem** at FANG+ companies because:

1. **Non-obvious optimization**: Brute force is O(nk), optimal is O(n)
2. **Deque mastery**: Tests understanding of double-ended queue operations
3. **Monotonic property**: Combines queue structure with monotonic invariant
4. **Real-world applications**: Rate limiting, time-series analysis, streaming data

Interviewers use this to assess your ability to optimize beyond the naive approach.

---

## The Problem

Given an array and sliding window size k, find the maximum value in each window as it slides from left to right.

```
Example:
nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3

Window position                Max
---------------               -----
[1  3  -1] -3  5  3  6  7       3
 1 [3  -1  -3] 5  3  6  7       3
 1  3 [-1  -3  5] 3  6  7       5
 1  3  -1 [-3  5  3] 6  7       5
 1  3  -1  -3 [5  3  6] 7       6
 1  3  -1  -3  5 [3  6  7]      7

Output: [3, 3, 5, 5, 6, 7]
```

---

## Approach Comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Brute force | O(n·k) | O(1) | Check all k elements for each window |
| Heap | O(n log k) | O(k) | Max heap with lazy deletion |
| Monotonic Deque | O(n) | O(k) | Optimal solution |

---

## Core Concept: Monotonic Deque

A monotonic deque maintains elements in decreasing order (front to back). The front always holds the current maximum.

```
Key insight: If nums[i] >= nums[j] and i > j, then nums[j] can never be
the maximum of any window that includes nums[i].

Example with nums = [1, 3, -1, -3, 5], k = 3

i=0: deque = [0]           (indices: 0, values: 1)
i=1: pop 0 (1 < 3)
     deque = [1]           (indices: 1, values: 3)
i=2: deque = [1, 2]        (indices: 1,2, values: 3,-1)
     window [0,1,2], max = nums[1] = 3

i=3: deque = [1, 2, 3]     (indices: 1,2,3, values: 3,-1,-3)
     check: 1 < 3-3+1=1, so keep (front in window)
     window [1,2,3], max = nums[1] = 3

i=4: pop 3 (-3 < 5)
     pop 2 (-1 < 5)
     pop 1 (3 < 5)
     deque = [4]           (indices: 4, values: 5)
     window [2,3,4], max = nums[4] = 5
```

---

## Optimal Solution

```python
from collections import deque

def max_sliding_window(nums: list[int], k: int) -> list[int]:
    """
    Find maximum in each sliding window of size k.

    LeetCode 239: Sliding Window Maximum

    Time: O(n) - each element added and removed at most once
    Space: O(k) - deque stores at most k indices
    """
    if not nums or k == 0:
        return []

    dq = deque()  # Store indices, values are monotonic decreasing
    result = []

    for i in range(len(nums)):
        # Remove indices outside current window
        while dq and dq[0] < i - k + 1:
            dq.popleft()

        # Remove smaller elements (they'll never be max)
        while dq and nums[dq[-1]] < nums[i]:
            dq.pop()

        dq.append(i)

        # Window is complete, record maximum
        if i >= k - 1:
            result.append(nums[dq[0]])

    return result


# Example
nums = [1, 3, -1, -3, 5, 3, 6, 7]
print(max_sliding_window(nums, 3))
# [3, 3, 5, 5, 6, 7]
```

### Step-by-Step Walkthrough

```
nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3

i=0, nums[i]=1
  dq = [0]                     # Push index 0

i=1, nums[i]=3
  dq = [0], 1 < 3, pop 0       # 1 < 3, remove it
  dq = [1]                     # Push index 1

i=2, nums[i]=-1
  dq = [1, 2]                  # -1 < 3, just push
  Window [0,1,2] complete
  result = [3]                 # max = nums[1] = 3

i=3, nums[i]=-3
  dq[0]=1 >= 3-3+1=1 ✓        # Front still in window
  dq = [1, 2, 3]              # -3 < -1, just push
  result = [3, 3]             # max = nums[1] = 3

i=4, nums[i]=5
  dq[0]=1 >= 4-3+1=2 ✗        # Front out of window, remove
  dq = [2, 3]
  dq = [2], pop 3 (-3 < 5)
  dq = [], pop 2 (-1 < 5)
  dq = [4]                    # Push index 4
  result = [3, 3, 5]          # max = nums[4] = 5

i=5, nums[i]=3
  dq = [4, 5]                 # 3 < 5, just push
  result = [3, 3, 5, 5]

i=6, nums[i]=6
  dq = [4], pop 5 (3 < 6)
  dq = [], pop 4 (5 < 6)
  dq = [6]
  result = [3, 3, 5, 5, 6]

i=7, nums[i]=7
  dq = [], pop 6 (6 < 7)
  dq = [7]
  result = [3, 3, 5, 5, 6, 7]
```

---

## Sliding Window Minimum

Just flip the comparison - remove larger elements instead.

```python
from collections import deque

def min_sliding_window(nums: list[int], k: int) -> list[int]:
    """
    Find minimum in each sliding window of size k.

    Time: O(n)
    Space: O(k)
    """
    if not nums or k == 0:
        return []

    dq = deque()  # Store indices, values are monotonic increasing
    result = []

    for i in range(len(nums)):
        # Remove indices outside current window
        while dq and dq[0] < i - k + 1:
            dq.popleft()

        # Remove larger elements (they'll never be min)
        while dq and nums[dq[-1]] > nums[i]:
            dq.pop()

        dq.append(i)

        if i >= k - 1:
            result.append(nums[dq[0]])

    return result


# Example
print(min_sliding_window([1, 3, -1, -3, 5, 3, 6, 7], 3))
# [-1, -3, -3, -3, 3, 3]
```

---

## Alternative: Heap Approach

```python
import heapq

def max_sliding_window_heap(nums: list[int], k: int) -> list[int]:
    """
    Sliding window max using heap with lazy deletion.

    Time: O(n log n) worst case, O(n log k) average
    Space: O(n) worst case for heap
    """
    if not nums or k == 0:
        return []

    # Max heap using negative values
    heap = []
    result = []

    for i in range(len(nums)):
        heapq.heappush(heap, (-nums[i], i))

        if i >= k - 1:
            # Lazy deletion: remove elements outside window
            while heap[0][1] < i - k + 1:
                heapq.heappop(heap)
            result.append(-heap[0][0])

    return result
```

---

## Application: Shortest Subarray with Sum at Least K

```python
from collections import deque

def shortest_subarray(nums: list[int], k: int) -> int:
    """
    Find shortest subarray with sum >= k (can have negatives).

    LeetCode 862: Shortest Subarray with Sum at Least K

    Time: O(n)
    Space: O(n)
    """
    n = len(nums)

    # Prefix sums
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + nums[i]

    result = float('inf')
    dq = deque()  # Monotonic increasing of prefix values

    for i in range(n + 1):
        # Check if we found a valid subarray
        while dq and prefix[i] - prefix[dq[0]] >= k:
            result = min(result, i - dq.popleft())

        # Maintain monotonic increasing property
        while dq and prefix[dq[-1]] >= prefix[i]:
            dq.pop()

        dq.append(i)

    return result if result != float('inf') else -1


# Example
print(shortest_subarray([2, -1, 2], 3))  # 3
print(shortest_subarray([1], 1))          # 1
print(shortest_subarray([1, 2], 4))       # -1
```

---

## Application: Jump Game VI

```python
from collections import deque

def max_result(nums: list[int], k: int) -> int:
    """
    Max sum path where you can jump at most k steps.

    LeetCode 1696: Jump Game VI

    Time: O(n)
    Space: O(k)
    """
    n = len(nums)
    dp = [0] * n
    dp[0] = nums[0]
    dq = deque([0])  # Monotonic decreasing of dp values

    for i in range(1, n):
        # Remove indices outside jump range
        while dq and dq[0] < i - k:
            dq.popleft()

        # Best we can do reaching position i
        dp[i] = dp[dq[0]] + nums[i]

        # Maintain monotonic decreasing
        while dq and dp[dq[-1]] <= dp[i]:
            dq.pop()

        dq.append(i)

    return dp[n - 1]


# Example
print(max_result([1, -1, -2, 4, -7, 3], 2))  # 7
# Path: 1 -> -1 -> 4 -> 3 = 7
```

---

## Application: Constrained Subsequence Sum

```python
from collections import deque

def constrained_subset_sum(nums: list[int], k: int) -> int:
    """
    Max sum of subsequence where adjacent elements are at most k apart.

    LeetCode 1425: Constrained Subsequence Sum

    Time: O(n)
    Space: O(k)
    """
    n = len(nums)
    dp = nums[:]  # dp[i] = max sum ending at i
    dq = deque()  # Monotonic decreasing of dp values

    for i in range(n):
        # Remove indices outside range
        while dq and dq[0] < i - k:
            dq.popleft()

        # Best previous value (if positive)
        if dq:
            dp[i] = max(dp[i], dp[dq[0]] + nums[i])

        # Maintain monotonic decreasing
        while dq and dp[dq[-1]] <= dp[i]:
            dq.pop()

        dq.append(i)

    return max(dp)


# Example
print(constrained_subset_sum([10, 2, -10, 5, 20], 2))  # 37
# Subsequence: [10, 2, 5, 20]
```

---

## Template: Monotonic Deque

```python
from collections import deque

def monotonic_deque_template(nums: list[int], k: int) -> list[int]:
    """
    Generic monotonic deque template for sliding window problems.
    """
    dq = deque()  # Store indices
    result = []

    for i in range(len(nums)):
        # Step 1: Remove elements outside window
        while dq and dq[0] < i - k + 1:
            dq.popleft()

        # Step 2: Remove elements that can't be answer
        # For max: remove smaller (nums[dq[-1]] < nums[i])
        # For min: remove larger (nums[dq[-1]] > nums[i])
        while dq and nums[dq[-1]] < nums[i]:
            dq.pop()

        # Step 3: Add current element
        dq.append(i)

        # Step 4: Record answer when window is complete
        if i >= k - 1:
            result.append(nums[dq[0]])

    return result
```

---

## Complexity Analysis

| Operation | Time | Notes |
|-----------|------|-------|
| Process n elements | O(n) | Each element added/removed once |
| Per element | O(1) amortized | Constant work on average |
| Space | O(k) | Deque stores at most k indices |

**Why O(n)?** Each index is added to deque exactly once and removed at most once (either from front when out of window, or from back when a larger element arrives). Total operations = 2n = O(n).

---

## Edge Cases

```python
# 1. Window size equals array length
nums = [1, 2, 3], k = 3
# Output: [3] (single window)

# 2. Window size is 1
nums = [1, 2, 3], k = 1
# Output: [1, 2, 3] (each element is its own window)

# 3. All same elements
nums = [5, 5, 5, 5], k = 2
# Output: [5, 5, 5]

# 4. Strictly increasing
nums = [1, 2, 3, 4, 5], k = 3
# Output: [3, 4, 5]

# 5. Strictly decreasing
nums = [5, 4, 3, 2, 1], k = 3
# Output: [5, 4, 3]
```

---

## Common Mistakes

1. **Using wrong end**: `popleft()` for window expiry, `pop()` for monotonic property
2. **Off-by-one**: Window starts recording at `i >= k - 1`, not `i >= k`
3. **Storing values vs indices**: Store indices to check window bounds
4. **Wrong comparison**: `<` for max, `>` for min

---

## Practice Problems

| # | Problem | Difficulty | Key Concept |
|---|---------|------------|-------------|
| 1 | Sliding Window Maximum | Hard | Core pattern |
| 2 | Shortest Subarray with Sum at Least K | Hard | Prefix sums + deque |
| 3 | Jump Game VI | Medium | DP optimization |
| 4 | Constrained Subsequence Sum | Hard | DP with deque |
| 5 | Longest Continuous Subarray With Abs Diff <= Limit | Medium | Two deques |
| 6 | Max Value of Equation | Hard | Deque optimization |

---

## Key Takeaways

1. **O(n) sliding window max/min**: Monotonic deque is the optimal approach
2. **Store indices**: Allows checking if element is within window
3. **Two removals**: Front for window expiry, back for monotonic property
4. **Deque operations**: `popleft()` and `pop()` both O(1)
5. **DP optimization**: Many DP problems with range constraints use this pattern

---

## Next: [06-min-stack.md](./06-min-stack.md)

Learn how to design a stack with O(1) getMin operation.
