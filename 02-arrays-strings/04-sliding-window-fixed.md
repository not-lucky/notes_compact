# Sliding Window: Fixed Size

> **Prerequisites:** [01-array-basics.md](./01-array-basics.md)

## Overview

Fixed-size sliding window maintains a window of exactly k elements that slides across an array. Instead of recalculating for each position (O(n×k)), we update incrementally—adding one element and removing another—achieving O(n).

## Building Intuition

**Why does sliding work so efficiently?**

The key insight is **incremental update**. Consecutive windows share almost all their elements:

1. **The Overlap Insight**: Window [0,k-1] and window [1,k] share elements [1,k-1]. Only two elements change: one leaves, one enters. Why recompute k elements when only 2 changed?

2. **Aggregate Functions**: Sum, count, frequency maps—all these can be updated incrementally. For sum: `new_sum = old_sum - leaving + entering`. This O(1) update is the heart of the technique.

3. **State Maintenance**: The "window state" (sum, max, frequency count, etc.) is maintained as the window slides. Each slide updates the state, not rebuilds it.

**Mental Model**: Think of a train with k cars. As the train moves forward, the rear car detaches and a new car attaches at the front. You don't need to count all passengers again—just subtract those who left and add those who joined.

**Brute Force vs Sliding Window**:
```
Brute Force:                    Sliding Window:
Window 1: sum([0:k])            Window 1: sum([0:k])
Window 2: sum([1:k+1])          Window 2: window_1 - arr[0] + arr[k]
Window 3: sum([2:k+2])          Window 3: window_2 - arr[1] + arr[k+1]
...                             ...
Each window: O(k)               Each slide: O(1)
Total: O(n×k)                   Total: O(n)
```

## When NOT to Use Fixed Sliding Window

Fixed windows have specific requirements:

1. **Variable Window Size Needed**: If the window size must change based on content (e.g., "smallest window containing X"), use variable-size sliding window instead.

2. **No Efficient Update Formula**: If the window "answer" can't be updated incrementally (e.g., median—adding/removing doesn't give new median easily), you may need a balanced BST or sorted container.

3. **k > n or k = 0**: Edge cases to handle—no valid window exists.

4. **Non-Contiguous Elements**: Sliding window requires contiguous subarrays. For non-contiguous subsequences, consider DP.

5. **Order Matters Differently**: If you need the k smallest elements (not a contiguous subarray of size k), use a heap instead.

**Red Flags:**
- "Minimum window size that satisfies..." → Variable window
- "k smallest/largest elements" → Heap, not window
- "Median of window" → Need ordered structure (heap pair or sorted list)

---

## Interview Context

Fixed-size sliding window problems are extremely common in FANG+ interviews because:

- They test your ability to optimize brute force O(n×k) to O(n)
- Easy to get wrong with off-by-one errors
- Foundation for understanding variable-size windows

Look for keywords: "subarray of size k", "contiguous k elements", "window of length k"

---

## Core Concept

Maintain a window of exactly k elements, sliding one position at a time:

```
Array: [1, 3, -1, -3, 5, 3, 6, 7], k = 3

Window slides:
[1, 3, -1] -3, 5, 3, 6, 7   → process window
1, [3, -1, -3] 5, 3, 6, 7   → slide right
1, 3, [-1, -3, 5] 3, 6, 7   → slide right
...

Key insight: Instead of recalculating for each window,
UPDATE the window state by:
- Adding the new element (entering window)
- Removing the old element (leaving window)
```

---

## Template: Maximum Sum of Subarray of Size K

```python
def max_sum_subarray_k(arr: list[int], k: int) -> int:
    """
    Find maximum sum of any contiguous subarray of size k.

    Time: O(n) - single pass
    Space: O(1)

    Example:
    arr = [2, 1, 5, 1, 3, 2], k = 3
    → 9 (subarray [5, 1, 3])
    """
    if len(arr) < k:
        return 0

    # Calculate sum of first window
    window_sum = sum(arr[:k])
    max_sum = window_sum

    # Slide the window
    for i in range(k, len(arr)):
        window_sum += arr[i]      # Add incoming element
        window_sum -= arr[i - k]  # Remove outgoing element
        max_sum = max(max_sum, window_sum)

    return max_sum
```

### Visual Trace

```
arr = [2, 1, 5, 1, 3, 2], k = 3

Step 0: [2, 1, 5] 1, 3, 2
        window_sum = 8, max = 8

Step 1: 2, [1, 5, 1] 3, 2
        window_sum = 8 + 1 - 2 = 7, max = 8

Step 2: 2, 1, [5, 1, 3] 2
        window_sum = 7 + 3 - 1 = 9, max = 9 ✓

Step 3: 2, 1, 5, [1, 3, 2]
        window_sum = 9 + 2 - 5 = 6, max = 9

Return 9
```

---

## Template: Average of Subarrays of Size K

```python
def average_of_subarrays(arr: list[int], k: int) -> list[float]:
    """
    Find average of all contiguous subarrays of size k.

    Time: O(n)
    Space: O(n-k+1) for output

    Example:
    arr = [1, 3, 2, 6, -1, 4, 1, 8, 2], k = 5
    → [2.2, 2.8, 2.4, 3.6, 2.8]
    """
    result = []
    window_sum = sum(arr[:k])
    result.append(window_sum / k)

    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]
        result.append(window_sum / k)

    return result
```

---

## Template: Maximum of Each Window (with Deque)

```python
from collections import deque

def max_sliding_window(arr: list[int], k: int) -> list[int]:
    """
    Find maximum element in each sliding window of size k.

    Time: O(n) - each element added/removed from deque once
    Space: O(k) for deque

    Example:
    arr = [1, 3, -1, -3, 5, 3, 6, 7], k = 3
    → [3, 3, 5, 5, 6, 7]
    """
    if not arr or k == 0:
        return []

    dq = deque()  # Stores indices, front is always max
    result = []

    for i in range(len(arr)):
        # Remove indices outside current window
        while dq and dq[0] < i - k + 1:
            dq.popleft()

        # Remove smaller elements (they can never be max)
        while dq and arr[dq[-1]] < arr[i]:
            dq.pop()

        dq.append(i)

        # Window is complete (i >= k-1)
        if i >= k - 1:
            result.append(arr[dq[0]])

    return result
```

### Why Deque Works

```
Maintaining a monotonic decreasing deque:

arr = [1, 3, -1, -3, 5, 3, 6, 7], k = 3

i=0: dq=[0]           (val 1)
i=1: dq=[1]           (3 > 1, pop 0, add 1)
i=2: dq=[1, 2]        (add 2, -1 < 3)
     Window [0-2]: max = arr[1] = 3

i=3: dq=[1, 2, 3]     (add 3, -3 < -1)
     Window [1-3]: max = arr[1] = 3

i=4: dq=[4]           (5 > all, clear and add 4)
     Window [2-4]: max = arr[4] = 5

Key: dq is always sorted descending by value,
     so front is always the maximum.
```

---

## Template: Contains Duplicate Within K Distance

```python
def contains_nearby_duplicate(arr: list[int], k: int) -> bool:
    """
    Check if there are duplicates within k positions.

    Time: O(n)
    Space: O(min(n, k))

    Example:
    arr = [1, 2, 3, 1], k = 3 → True (indices 0 and 3)
    arr = [1, 2, 3, 1, 2, 3], k = 2 → False
    """
    window = set()

    for i, num in enumerate(arr):
        if num in window:
            return True

        window.add(num)

        # Remove element leaving the window
        if i >= k:
            window.remove(arr[i - k])

    return False
```

---

## Template: Count Distinct Elements in Window

```python
def distinct_in_windows(arr: list[int], k: int) -> list[int]:
    """
    Count distinct elements in each window of size k.

    Time: O(n)
    Space: O(k)

    Example:
    arr = [1, 2, 1, 3, 4, 2, 3], k = 4
    → [3, 4, 4, 3]  (windows: [1,2,1,3], [2,1,3,4], [1,3,4,2], [3,4,2,3])
    """
    from collections import Counter

    result = []
    count = Counter(arr[:k])
    result.append(len(count))

    for i in range(k, len(arr)):
        # Add new element
        count[arr[i]] += 1

        # Remove old element
        count[arr[i - k]] -= 1
        if count[arr[i - k]] == 0:
            del count[arr[i - k]]

        result.append(len(count))

    return result
```

---

## Template: Find All Anagrams

```python
def find_anagrams(s: str, p: str) -> list[int]:
    """
    Find starting indices of p's anagrams in s.
    Window size = len(p).

    Time: O(n) where n = len(s)
    Space: O(1) - at most 26 characters

    Example:
    s = "cbaebabacd", p = "abc"
    → [0, 6]  (substrings "cba" and "bac")
    """
    if len(p) > len(s):
        return []

    result = []
    p_count = {}
    window_count = {}

    # Build target frequency map
    for c in p:
        p_count[c] = p_count.get(c, 0) + 1

    k = len(p)

    for i in range(len(s)):
        # Add character to window
        c = s[i]
        window_count[c] = window_count.get(c, 0) + 1

        # Remove character leaving window
        if i >= k:
            old = s[i - k]
            window_count[old] -= 1
            if window_count[old] == 0:
                del window_count[old]

        # Check if window matches
        if window_count == p_count:
            result.append(i - k + 1)

    return result
```

---

## Alternative: Using Array Instead of HashMap

For problems with limited character set (lowercase letters):

```python
def find_anagrams_array(s: str, p: str) -> list[int]:
    """
    Same as above but using array for O(1) comparison.

    Time: O(n × 26) ≈ O(n)
    Space: O(26) = O(1)
    """
    if len(p) > len(s):
        return []

    result = []
    p_count = [0] * 26
    window_count = [0] * 26

    for c in p:
        p_count[ord(c) - ord('a')] += 1

    k = len(p)

    for i in range(len(s)):
        window_count[ord(s[i]) - ord('a')] += 1

        if i >= k:
            window_count[ord(s[i - k]) - ord('a')] -= 1

        if window_count == p_count:
            result.append(i - k + 1)

    return result
```

---

## Edge Cases

```python
# k larger than array
len(arr) < k → return 0/[] or handle specially

# k = 1
Each element is its own window

# k = len(arr)
Only one window (entire array)

# All same elements
Every window has same sum/max

# Negative numbers
Still works with sum technique

# Empty array
Return 0 or []
```

---

## Brute Force vs Sliding Window Comparison

```
Brute Force (O(n × k)):
for i in range(n - k + 1):
    window_sum = sum(arr[i:i+k])  # O(k) each time
    ...

Sliding Window (O(n)):
window_sum = sum(arr[:k])        # O(k) once
for i in range(k, n):
    window_sum += arr[i] - arr[i-k]  # O(1) each time
    ...
```

---

## Practice Problems

| # | Problem | Difficulty | Key Technique |
|---|---------|------------|---------------|
| 1 | Maximum Sum Subarray of Size K | Easy | Basic sliding sum |
| 2 | Maximum Average Subarray I | Easy | Sum → average |
| 3 | Find All Anagrams in a String | Medium | Frequency matching |
| 4 | Permutation in String | Medium | Same as anagrams |
| 5 | Sliding Window Maximum | Hard | Monotonic deque |
| 6 | Contains Duplicate II | Easy | HashSet window |
| 7 | Repeated DNA Sequences | Medium | Hash of window |

---

## Key Takeaways

1. **Add new, remove old** - core sliding window update
2. **Initialize first window** before sliding
3. **Index arithmetic**: new element at `i`, old element at `i - k`
4. **Use appropriate data structure**: sum, set, map, deque
5. **Deque for min/max** - maintain monotonic order

---

## Next: [05-sliding-window-variable.md](./05-sliding-window-variable.md)

Learn variable-size windows for substring and optimization problems.
