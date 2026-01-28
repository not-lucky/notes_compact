# Sliding Window: Variable Size

> **Prerequisites:** [04-sliding-window-fixed.md](./04-sliding-window-fixed.md)

## Overview

Variable-size sliding window expands and shrinks based on conditions, finding optimal contiguous subarrays. This pattern solves "longest/shortest subarray satisfying X" problems in O(n) where brute force would be O(n²) or O(n³).

## Building Intuition

**Why does the expand/shrink approach work?**

The key insight is **monotonic progress**. Both pointers only move forward, guaranteeing O(n) total moves:

1. **The Expand-Shrink Dance**: The right pointer expands the window, adding elements until a condition is met (or violated). Then the left pointer shrinks, removing elements until the condition flips. This dance explores all viable windows without revisiting combinations.

2. **Why We Don't Miss Windows**: Every possible window has some right endpoint. By expanding right systematically and shrinking left optimally for each right position, we implicitly consider all windows. The left pointer never moves backward because shrinking past the optimal point for one right endpoint would only make future windows worse.

3. **Maximum vs Minimum Windows**:
   - **Maximum valid window**: Shrink when window becomes invalid. We want the largest valid window.
   - **Minimum valid window**: Shrink while window stays valid. We want the smallest valid window.

**Mental Model**: Imagine an accordion. You stretch it open (expand right), and when it gets too wide to handle, you compress the left side (shrink left). You're looking for either the widest manageable stretch or the narrowest sufficient stretch.

**The Two Scenarios**:

```
For MAXIMUM valid window:
  - Keep expanding right
  - When INVALID: shrink left until valid again
  - Track max during valid states

For MINIMUM valid window:
  - Keep expanding right
  - When VALID: record answer, then shrink left (still valid? record again!)
  - Stop shrinking when invalid
```

## When NOT to Use Variable Sliding Window

This pattern has important limitations:

1. **Negative Numbers with Sum Constraints**: Sliding window assumes adding elements increases (or maintains) some measure and removing decreases it. With negative numbers, adding an element might decrease sum. Use prefix sum + hash map instead.

2. **Non-Contiguous Subsequences**: Sliding window finds contiguous subarrays only. For subsequences (elements not necessarily adjacent), use DP or two-pointer on sorted data.

3. **Complex Validity That Isn't Monotonic**: If validity doesn't behave monotonically (valid→add→maybe invalid, invalid→remove→maybe valid), sliding window can't be applied directly.

4. **Multiple Non-Overlapping Windows**: If you need multiple disjoint windows (like "partition into k subarrays"), this is interval DP or greedy, not sliding window.

5. **When Window State Is Expensive**: If updating window state isn't O(1) (e.g., maintaining sorted order), the O(n) guarantee breaks.

**Red Flags:**

- "Subarray sum = k" with negative numbers → Prefix sum + hash map
- "Subsequence" (not substring/subarray) → Usually DP
- "Partition array into..." → Interval DP or greedy
- "Median of all subarrays" → O(n²) or special data structures

---

## Interview Context

Variable-size sliding window is arguably the **most important pattern** for string problems at FANG+. It appears in:

- Substring problems
- Subarray with target sum
- Minimum/maximum length problems
- String matching and containment

This pattern alone covers 20-30% of medium/hard string problems.

---

## Core Concept

The window expands and shrinks based on a condition:

```
Expand window (move right pointer):
- When condition NOT satisfied yet
- When looking for longer valid window

Shrink window (move left pointer):
- When condition is satisfied (for minimum)
- When condition is violated (for maximum)

Key insight: At each step, either expand OR shrink (never both)
```

---

## Template: Longest Substring Without Repeating

```python
def length_of_longest_substring(s: str) -> int:
    """
    Find length of longest substring without repeating characters.

    Time: O(n)
    Space: O(min(n, alphabet_size))

    Example:
    "abcabcbb" → 3 ("abc")
    "bbbbb" → 1 ("b")
    """
    char_index = {}  # Last seen index of each character
    left = 0
    max_length = 0

    for right in range(len(s)):
        char = s[right]

        # If char in window, shrink from left
        if char in char_index and char_index[char] >= left:
            left = char_index[char] + 1

        char_index[char] = right
        max_length = max(max_length, right - left + 1)

    return max_length
```

### Visual Trace

```
s = "abcabcbb"

right=0 'a': window="a", left=0, max=1
right=1 'b': window="ab", left=0, max=2
right=2 'c': window="abc", left=0, max=3
right=3 'a': 'a' at index 0 in window, left=1
             window="bca", max=3
right=4 'b': 'b' at index 1 in window, left=2
             window="cab", max=3
right=5 'c': 'c' at index 2 in window, left=3
             window="abc", max=3
right=6 'b': 'b' at index 4 in window, left=5
             window="cb", max=3
right=7 'b': 'b' at index 6 in window, left=7
             window="b", max=3

Return 3
```

---

## Template: Minimum Window Substring

```python
def min_window(s: str, t: str) -> str:
    """
    Find minimum window in s containing all characters of t.

    Time: O(n + m) where n = len(s), m = len(t)
    Space: O(m) for frequency maps

    Example:
    s = "ADOBECODEBANC", t = "ABC"
    → "BANC"
    """
    if not s or not t:
        return ""

    from collections import Counter

    need = Counter(t)        # Characters we need
    have = {}                # Characters we have in window
    need_count = len(need)   # Unique chars needed
    have_count = 0           # Unique chars satisfied

    left = 0
    min_len = float('inf')
    result = ""

    for right in range(len(s)):
        char = s[right]

        # Expand: add char to window
        have[char] = have.get(char, 0) + 1

        # Check if this char is now satisfied
        if char in need and have[char] == need[char]:
            have_count += 1

        # Shrink: while window is valid, try to minimize
        while have_count == need_count:
            # Update result if smaller
            if right - left + 1 < min_len:
                min_len = right - left + 1
                result = s[left:right + 1]

            # Remove leftmost char
            left_char = s[left]
            have[left_char] -= 1

            if left_char in need and have[left_char] < need[left_char]:
                have_count -= 1

            left += 1

    return result
```

### Why This Works

```
Two counters track validity:
- need_count: number of unique characters required
- have_count: number of unique characters we have enough of

Expand until have_count == need_count (valid window)
Then shrink while maintaining validity to find minimum
```

---

## Template: Longest Substring with At Most K Distinct Characters

```python
def longest_k_distinct(s: str, k: int) -> int:
    """
    Longest substring with at most k distinct characters.

    Time: O(n)
    Space: O(k)

    Example:
    s = "eceba", k = 2 → 3 ("ece")
    s = "aa", k = 1 → 2 ("aa")
    """
    from collections import Counter

    char_count = Counter()
    left = 0
    max_length = 0

    for right in range(len(s)):
        char_count[s[right]] += 1

        # Shrink while more than k distinct
        while len(char_count) > k:
            char_count[s[left]] -= 1
            if char_count[s[left]] == 0:
                del char_count[s[left]]
            left += 1

        max_length = max(max_length, right - left + 1)

    return max_length
```

---

## Template: Longest Repeating Character Replacement

```python
def character_replacement(s: str, k: int) -> int:
    """
    Longest substring with same letter after replacing at most k chars.

    Time: O(n)
    Space: O(26) = O(1)

    Example:
    s = "AABABBA", k = 1 → 4 ("AABA" → "AAAA")
    """
    count = {}
    left = 0
    max_count = 0  # Max frequency of any single char in window
    max_length = 0

    for right in range(len(s)):
        count[s[right]] = count.get(s[right], 0) + 1
        max_count = max(max_count, count[s[right]])

        # Window is valid if: window_size - max_count <= k
        # (chars to replace <= k)
        window_size = right - left + 1

        if window_size - max_count > k:
            # Invalid: shrink
            count[s[left]] -= 1
            left += 1
        else:
            max_length = max(max_length, window_size)

    return max_length
```

### Key Insight

```
Window [left, right] is valid if:
  window_length - most_frequent_char_count <= k

We can replace (window_length - most_frequent) characters to make all same.
If this exceeds k, window is invalid → shrink.
```

---

## Template: Subarray Sum Equals K (Prefix Sum + HashMap)

```python
def subarray_sum(nums: list[int], k: int) -> int:
    """
    Count subarrays with sum equal to k.

    Note: This is NOT sliding window (handles negatives).
    Uses prefix sum with hashmap.

    Time: O(n)
    Space: O(n)

    Example:
    nums = [1, 1, 1], k = 2 → 2
    """
    count = 0
    prefix_sum = 0
    prefix_count = {0: 1}  # prefix_sum → count

    for num in nums:
        prefix_sum += num

        # If prefix_sum - k exists, we found subarrays
        if prefix_sum - k in prefix_count:
            count += prefix_count[prefix_sum - k]

        prefix_count[prefix_sum] = prefix_count.get(prefix_sum, 0) + 1

    return count
```

---

## Template: Minimum Size Subarray Sum

```python
def min_subarray_len(target: int, nums: list[int]) -> int:
    """
    Minimum length subarray with sum >= target.
    All positive numbers.

    Time: O(n)
    Space: O(1)

    Example:
    target = 7, nums = [2, 3, 1, 2, 4, 3] → 2 ([4, 3])
    """
    left = 0
    current_sum = 0
    min_length = float('inf')

    for right in range(len(nums)):
        current_sum += nums[right]

        # Shrink while condition met
        while current_sum >= target:
            min_length = min(min_length, right - left + 1)
            current_sum -= nums[left]
            left += 1

    return min_length if min_length != float('inf') else 0
```

---

## General Template

```python
def sliding_window_variable(arr, condition_func):
    """
    General template for variable-size sliding window.

    For MAXIMUM valid window:
    - Expand while valid
    - When invalid, shrink until valid again

    For MINIMUM valid window:
    - Expand until valid
    - While valid, shrink and track minimum
    """
    left = 0
    result = 0  # or float('inf') for minimum
    window_state = {}  # whatever state you need

    for right in range(len(arr)):
        # 1. EXPAND: Add arr[right] to window state
        update_window_state(window_state, arr[right])

        # 2. SHRINK: Remove elements until window is valid
        while not is_valid(window_state):  # or while is_valid() for minimum
            remove_from_state(window_state, arr[left])
            left += 1

        # 3. UPDATE result
        result = max(result, right - left + 1)  # or track minimum

    return result
```

---

## When to Use Which Technique

| Problem Type                  | Technique        | Example                   |
| ----------------------------- | ---------------- | ------------------------- |
| Longest with constraint       | Variable window  | Longest without repeating |
| Shortest containing           | Variable window  | Minimum window substring  |
| Fixed size aggregation        | Fixed window     | Max sum of k elements     |
| Sum equals target (negatives) | Prefix sum + map | Subarray sum = k          |
| Sum equals target (positives) | Variable window  | Min subarray sum >= k     |

---

## Edge Cases

```python
# Empty string/array
"" → 0

# Single character
"a" → 1 (or based on problem)

# k = 0
Usually return 0 or ""

# All same characters
"aaaa" → length of string (often)

# No valid window exists
Return 0 or ""
```

---

## Common Mistakes

1. **Not handling the shrink correctly** - forgetting to update state
2. **Off-by-one in window size** - `right - left + 1` not `right - left`
3. **Using sliding window for negative numbers** - need prefix sum instead
4. **Not initializing left = 0**
5. **Updating result at wrong time** - before or after shrinking?

---

## Practice Problems

| #   | Problem                                        | Difficulty | Pattern             |
| --- | ---------------------------------------------- | ---------- | ------------------- |
| 1   | Longest Substring Without Repeating Characters | Medium     | Set/Map window      |
| 2   | Minimum Window Substring                       | Hard       | Character matching  |
| 3   | Longest Substring with At Most K Distinct      | Medium     | Counter window      |
| 4   | Longest Repeating Character Replacement        | Medium     | Max count tracking  |
| 5   | Fruit Into Baskets                             | Medium     | At most 2 distinct  |
| 6   | Subarray Product Less Than K                   | Medium     | Product window      |
| 7   | Minimum Size Subarray Sum                      | Medium     | Sum >= target       |
| 8   | Maximum Erasure Value                          | Medium     | Unique elements sum |

---

## Key Takeaways

1. **Expand right pointer unconditionally**
2. **Shrink left pointer conditionally** (based on validity)
3. **For maximum**: shrink when invalid
4. **For minimum**: shrink while valid
5. **Track window state** with appropriate data structure
6. **Sliding window needs monotonic property** (positive numbers for sum)

---

## Next: [06-prefix-sum.md](./06-prefix-sum.md)

Learn prefix sums for O(1) range queries.
