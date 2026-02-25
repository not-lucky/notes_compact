# Sliding Window: Fixed Size

> **Prerequisites:** [01-array-basics.md](./01-array-basics.md)

## Overview

A fixed-size sliding window maintains a window of exactly $k$ elements that slides across an array or string. Instead of recalculating the required metric for each position from scratch (which takes $O(n \times k)$ time), we update the metric incrementally. By adding the effect of one entering element and removing the effect of one leaving element, we achieve an optimal $\Theta(n)$ time complexity.

## Building Intuition

**Why does sliding work so efficiently?**

The key insight is **incremental update**. Consecutive windows share almost all of their elements:

1. **The Overlap Insight**: The window at index `0` (elements `[0, k-1]`) and the window at index `1` (elements `[1, k]`) share the elements `[1, k-1]`. Only two elements change: one leaves the window (at index `0`), and one enters (at index `k`). Why recompute $k$ elements when only 2 changed?
2. **Aggregate Functions**: Sums, counts, and frequency maps can all be updated incrementally. For a sum: `new_sum = old_sum - leaving + entering`. This $\Theta(1)$ update is the heart of the technique.
3. **State Maintenance**: The "window state" (sum, maximum, frequency count, etc.) is maintained as the window slides. Each slide updates the state rather than rebuilding it.

**Mental Model**: Think of a train with exactly $k$ cars moving along a track. As the train moves forward by one position, the rear car detaches and is left behind, while a new car attaches at the front. If you want to know the total weight of the train, you don't need to weigh all $k$ cars again—just subtract the weight of the car that detached and add the weight of the newly attached car.

**Brute Force vs Sliding Window**:

```text
Brute Force:                    Sliding Window:
Window 1: sum([0:k])            Window 1: sum([0:k])
Window 2: sum([1:k+1])          Window 2: window_1 - arr[0] + arr[k]
Window 3: sum([2:k+2])          Window 3: window_2 - arr[1] + arr[k+1]
...                             ...
Each window: O(k)               Each slide: O(1)
Total Time: O(n × k)            Total Time: Θ(n)
```

## When NOT to Use Fixed Sliding Window

Fixed windows have specific requirements. Watch out for these red flags:

1. **Variable Window Size Needed**: If the window size must change based on content (e.g., "smallest window containing X" or "longest substring with at most 2 distinct characters"), use the **variable-size sliding window** instead.
2. **No Efficient Update Formula**: If the window "answer" cannot be updated incrementally in $O(1)$ or $O(\log k)$ time (e.g., finding the median—adding/removing an element doesn't yield the new median easily), you may need a more advanced structure like a balanced BST, two heaps, or a sorted container.
3. **$k > n$ or $k \le 0$**: These are edge cases where no valid window exists or the logic breaks down.
4. **Non-Contiguous Elements**: The sliding window technique strictly requires contiguous subarrays or substrings. For non-contiguous subsequences, consider Dynamic Programming or Backtracking.
5. **Order Matters Differently**: If you need the $k$ smallest elements overall (not a contiguous subarray of size $k$), use a Heap instead.

**Red Flags:**
- "Minimum window size that satisfies..." $\rightarrow$ Variable window
- "k smallest/largest elements" $\rightarrow$ Heap, not window
- "Median of window" $\rightarrow$ Ordered structure (two heaps or sorted list)

---

## Interview Context

Fixed-size sliding window problems are extremely common in FANG+ interviews because:

- They test your ability to optimize a brute force $O(n \times k)$ approach to a tight bound of $\Theta(n)$.
- They are easy to get wrong with off-by-one errors (e.g., `i - k` vs `i - k + 1`).
- They form the foundation for understanding the more complex variable-size window patterns.

**Look for keywords**: "subarray of size $k$", "contiguous $k$ elements", "substring of length $k$"

---

## Core Concept

Maintain a window of exactly $k$ elements, sliding one position at a time:

```text
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

### Problem: Maximum Sum Subarray of Size K
**Problem Statement:** Given an array of positive numbers and a positive number `k`, find the maximum sum of any contiguous subarray of size `k`.

**Why it works:**
The sum of a subarray of size `k` ending at index `i` is $S_{i}$. The sum ending at index `i+1` is $S_{i+1} = S_{i} - \text{arr}[i-k+1] + \text{arr}[i+1]$.
1. Calculate the initial sum for the first `k` elements.
2. Slide the window by subtracting the element that is falling out and adding the element that is coming in.

```python
def max_sum_subarray_k(arr: list[int], k: int) -> int:
    """
    Find maximum sum of any contiguous subarray of size k.

    Time Complexity: Θ(n) - exactly one pass through the array.
    Space Complexity: Θ(1) - only primitive variables used.

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

```text
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

    Time Complexity: Θ(n)
    Space Complexity: Θ(n-k+1) for the output list.
    Note: Python lists are dynamic arrays, providing amortized O(1) append time.

    Example:
    arr = [1, 3, 2, 6, -1, 4, 1, 8, 2], k = 5
    → [2.2, 2.8, 2.4, 3.6, 2.8]
    """
    if len(arr) < k:
        return []

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

### Problem: Sliding Window Maximum
**Problem Statement:** You are given an array of integers `nums`, there is a sliding window of size `k` which is moving from the very left of the array to the very right. Return the max sliding window.

**Why it works:**
We use a monotonic decreasing double-ended queue (`deque`) to keep track of the maximum.
1. The deque stores **indices** of elements that are potential candidates for the maximum of the current or future windows.
2. When a new element comes, we remove all elements smaller than it from the back of the deque because they can never be the maximum again (the new element is larger and will stay in the window longer).
3. The element at the front of the deque is always the maximum for the current window.
This ensures each element is added and removed at most once, achieving strict $\Theta(n)$ time.

```python
from collections import deque

def max_sliding_window(arr: list[int], k: int) -> list[int]:
    """
    Find maximum element in each sliding window of size k.

    Time Complexity: Θ(n) - each element is pushed/popped from deque at most once.
    Space Complexity: O(k) for the deque, plus O(n-k+1) for the result array.

    Example:
    arr = [1, 3, -1, -3, 5, 3, 6, 7], k = 3
    → [3, 3, 5, 5, 6, 7]
    """
    if not arr or k == 0:
        return []

    dq = deque()  # Stores indices, front is always the max for current window
    result = []

    for i in range(len(arr)):
        # 1. Remove indices that are outside the current window of size k
        if dq and dq[0] < i - k + 1:
            dq.popleft()

        # 2. Remove smaller elements from the back (they can never be the maximum)
        while dq and arr[dq[-1]] < arr[i]:
            dq.pop()

        # 3. Add the current element's index
        dq.append(i)

        # 4. If the window has reached size k, record the maximum
        if i >= k - 1:
            result.append(arr[dq[0]])

    return result
```

### Why Deque Works

```text
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

Key insight: The deque is always sorted descending by the values the indices point to.
Therefore, the front (leftmost) element index always points to the window's maximum.
```

---

## Template: Contains Duplicate Within K Distance

### Problem: Contains Duplicate II
**Problem Statement:** Given an integer array `nums` and an integer `k`, return `true` if there are two distinct indices `i` and `j` in the array such that `nums[i] == nums[j]` and `abs(i - j) <= k`.

**Why it works:**
We maintain a hash set containing the last `k` elements.
1. As we iterate, if the current element is in the set, we've found a duplicate within distance `k`.
2. If not, we add it to the set and remove the element that is now more than `k` distance away (`arr[i-k]`).
The set acts as a "sliding window" for membership testing.

```python
def contains_nearby_duplicate(arr: list[int], k: int) -> bool:
    """
    Check if there are duplicates within k positions.

    Time Complexity: Amortized Θ(n). Set lookups/insertions/deletions are
                     amortized O(1), but can degrade to O(n) worst-case
                     due to hash collisions.
    Space Complexity: O(min(n, k)) to store at most k elements in the hash set.

    Example:
    arr = [1, 2, 3, 1], k = 3 → True (indices 0 and 3)
    arr = [1, 2, 3, 1, 2, 3], k = 2 → False
    """
    window = set()

    for i, num in enumerate(arr):
        if num in window:  # Amortized O(1) lookup
            return True

        window.add(num)    # Amortized O(1) insertion

        # Remove element leaving the window
        if i >= k:
            window.remove(arr[i - k])  # Amortized O(1) deletion

    return False
```

---

## Template: Count Distinct Elements in Window

```python
from collections import Counter

def distinct_in_windows(arr: list[int], k: int) -> list[int]:
    """
    Count distinct elements in each window of size k.

    Time Complexity: Amortized Θ(n) because Python's Counter (a subclass of dict)
                     provides amortized O(1) insertions/deletions. Worst-case is O(n^2)
                     if frequent hash collisions occur during the loop.
    Space Complexity: O(k) to store frequencies in the hash map, plus O(n-k+1)
                      for the result array.

    Example:
    arr = [1, 2, 1, 3, 4, 2, 3], k = 4
    → [3, 4, 4, 3]  (windows: [1,2,1,3], [2,1,3,4], [1,3,4,2], [3,4,2,3])
    """
    if not arr or k == 0:
        return []

    result = []
    count = Counter(arr[:k])
    result.append(len(count))

    for i in range(k, len(arr)):
        # Add new element entering the window
        count[arr[i]] += 1

        # Remove old element leaving the window
        count[arr[i - k]] -= 1
        if count[arr[i - k]] == 0:
            del count[arr[i - k]]

        result.append(len(count))

    return result
```

---

## Template: Find All Anagrams

### Problem: Find All Anagrams in a String
**Problem Statement:** Given two strings `s` and `p`, return an array of all the start indices of `p`'s anagrams in `s`.

**Why it works:**
An anagram must have the same length and same exact character frequencies.
1. The window size is fixed at `len(p)`.
2. We maintain a frequency count of characters in the current window of `s`.
3. If the window's count matches `p`'s count exactly, the current window is an anagram.
By updating the count incrementally, we avoid rebuilding the frequency map for every window.

```python
def find_anagrams(s: str, p: str) -> list[int]:
    """
    Find starting indices of p's anagrams in s.
    Window size = len(p).

    Time Complexity: Amortized Θ(n) where n = len(s). Dict comparisons take O(26) = O(1).
                     Worst-case time could be O(n) per dict operation under severe
                     hash collisions, making it O(n^2), though extremely rare.
    Space Complexity: O(1) auxiliary space - the dicts hold at most 26 characters.

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

    # Note: Using Python string slicing (e.g., s[i:i+k]) in a loop takes O(k) time per iteration,
    # leading to O(n * k). We avoid it by using indices and updating the dictionary directly.
    for i in range(len(s)):
        # Add character entering window
        c = s[i]
        window_count[c] = window_count.get(c, 0) + 1

        # Remove character leaving window
        if i >= k:
            old = s[i - k]
            window_count[old] -= 1
            if window_count[old] == 0:
                del window_count[old]

        # Check if window matches
        if window_count == p_count:  # O(26) comparison
            result.append(i - k + 1)

    return result
```

---

## Alternative: Using Array Instead of HashMap

For problems with a strictly limited character set (e.g., only lowercase English letters), an array of fixed size `26` is often faster in practice and avoids the worst-case hash collision risks of hash maps.

```python
def find_anagrams_array(s: str, p: str) -> list[int]:
    """
    Same logic as above but using an array of size 26 for guaranteed O(1) comparison.

    Time Complexity: Strict Θ(n). Array lookups and O(26) comparisons are
                     strictly constant time. No hash collision risks.
    Space Complexity: O(1) auxiliary space for the length 26 frequency arrays.
    """
    if len(p) > len(s):
        return []

    result = []
    p_count = [0] * 26
    window_count = [0] * 26

    # Initialize target frequencies
    for c in p:
        p_count[ord(c) - ord('a')] += 1

    k = len(p)

    for i in range(len(s)):
        # Add incoming character
        window_count[ord(s[i]) - ord('a')] += 1

        # Remove outgoing character
        if i >= k:
            window_count[ord(s[i - k]) - ord('a')] -= 1

        # Compare the two fixed-size arrays (O(26) -> O(1))
        if window_count == p_count:
            result.append(i - k + 1)

    return result
```

---

## Edge Cases

When implementing fixed sliding window, always watch out for:

```python
# k larger than array
if len(arr) < k: return 0  # or [] depending on expected return type

# k = 1
# Each element is its own window; often trivial but still works.

# k = len(arr)
# Only one valid window (the entire array).

# Empty array or string
# Should be caught by the len(arr) < k check if k >= 1.
```

---

## Practice Problems

| #   | Problem                        | Difficulty | Key Technique      |
| --- | ------------------------------ | ---------- | ------------------ |
| 1   | Maximum Sum Subarray of Size K | Easy       | Basic sliding sum  |
| 2   | Maximum Average Subarray I     | Easy       | Sum → average      |
| 3   | Find All Anagrams in a String  | Medium     | Frequency matching |
| 4   | Permutation in String          | Medium     | Same as anagrams   |
| 5   | Sliding Window Maximum         | Hard       | Monotonic deque    |
| 6   | Contains Duplicate II          | Easy       | HashSet window     |
| 7   | Repeated DNA Sequences         | Medium     | Hash of window     |

---

## Key Takeaways

1. **Add new, remove old**: The core update strategy to transition from an $O(n \times k)$ brute force to an optimal $\Theta(n)$ time complexity.
2. **Initialize the first window**: Usually compute the metric for indices `0` to `k-1` before entering the main sliding loop.
3. **Index arithmetic**: In a loop iterating with index `i`, the new element is at `i`, and the old element leaving the window is at `i - k`.
4. **Python performance nuance**: Hash maps (`dict`, `set`, `Counter`) offer amortized $O(1)$ operations but $O(n)$ worst-case. For small, fixed alphabets (like 26 lowercase letters), fixed-size arrays guarantee strict $O(1)$ operations without collision risks.
5. **Deque for min/max**: Maintain a monotonic order to find window minimums or maximums in $\Theta(n)$ time.

---

## Next: [05-sliding-window-variable.md](./05-sliding-window-variable.md)

Learn variable-size windows for substring and optimization problems.
