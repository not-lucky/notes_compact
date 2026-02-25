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

**Mental Model**: Imagine an accordion or a caterpillar. You stretch the caterpillar forward (expand right pointer) until it reaches for food. When it gets too stretched, it pulls its back end forward (shrink left pointer). You're continuously expanding and shrinking to find either the widest stretch (maximum) or the narrowest contraction (minimum) while keeping the insect happy (valid condition).

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

### Problem: Longest Substring Without Repeating Characters
**Problem Statement:** Given a string `s`, find the length of the longest substring without repeating characters.

**Why it works:**
We use a `right` pointer to expand our potential substring and a `left` pointer to shrink it whenever a duplicate is found.
1. We store the last seen index of each character in a hash map.
2. When the character at `right` is already in our map and its index is within our current window (`>= left`), it's a repeat.
3. We jump `left` to one position past the last occurrence of that character.
This ensures the window `[left, right]` always contains unique characters, and we record the maximum size achieved.

```python
def length_of_longest_substring(s: str) -> int:
    """
    Find length of longest substring without repeating characters.

    Time Complexity: O(n) where n is the length of string s. Each character
                     is processed at most twice (once by right, once by left pointer).
    Space Complexity: O(min(n, a)) where 'a' is the alphabet size (e.g., 26 or 128).
                      Hash map insertion/lookup is amortized O(1), but worst-case
                      O(n) if hash collisions occur (rare with Python's dict).

    Example:
    "abcabcbb" → 3 ("abc")
    "bbbbb" → 1 ("b")
    """
    char_index: dict[str, int] = {}  # Last seen index of each character
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

### Problem: Minimum Window Substring
**Problem Statement:** Given two strings `s` and `t` of lengths `m` and `n` respectively, return the minimum window substring of `s` such that every character in `t` (including duplicates) is included in the window.

**Why it works:**
This is a "minimum valid window" problem.
1. **Expand**: Move the `right` pointer until the window contains all characters in `t`.
2. **Shrink**: Once the window is valid, move the `left` pointer to find the smallest possible valid window ending at `right`.
3. We keep track of the minimum size found during these shrinking steps.
The `have_count` and `need_count` variables allow us to check validity in O(1) time after each expansion/shrinkage.

```python
def min_window(s: str, t: str) -> str:
    """
    Find minimum window in s containing all characters of t.

    Time Complexity: Θ(n + m) where n = len(s), m = len(t).
                     Every character is visited at most twice.
    Space Complexity: O(u) where 'u' is the number of unique characters in t (bounded by alphabet size).
                      Hash map updates/lookups are amortized O(1).

    Example:
    s = "ADOBECODEBANC", t = "ABC"
    → "BANC"
    """
    if not s or not t:
        return ""

    from collections import Counter

    need: dict[str, int] = Counter(t)        # Characters we need
    have: dict[str, int] = {}                # Characters we have in window
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

### Problem: Longest Substring with At Most K Distinct Characters
**Problem Statement:** Given a string `s` and an integer `k`, return the length of the longest substring of `s` that contains at most `k` distinct characters.

**Why it works:**
This is a "maximum valid window" problem.
1. **Expand**: Move `right` and add characters to a frequency map.
2. **Shrink**: If the number of distinct characters in the map exceeds `k`, move `left` and decrement counts until the number of distinct characters is back to `k`.
3. The size of each valid window `[left, right]` is compared to the `max_length`.
The monotonic expansion ensures we don't skip any potential longest substring.

```python
def longest_k_distinct(s: str, k: int) -> int:
    """
    Longest substring with at most k distinct characters.

    Time Complexity: Θ(n). Right pointer moves n times, left pointer moves
                     at most n times.
    Space Complexity: O(k) for the hash map storing character counts.
                      Note that Counter updates are amortized O(1).

    Example:
    s = "eceba", k = 2 → 3 ("ece")
    s = "aa", k = 1 → 2 ("aa")
    """
    from collections import Counter

    char_count: Counter[str] = Counter()
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

### Problem: Longest Repeating Character Replacement
**Problem Statement:** You are given a string `s` and an integer `k`. You can choose any character of the string and change it to any other uppercase English character. You can perform this operation at most `k` times. Return the length of the longest substring containing the same letter you can get after performing the above operations.

**Why it works:**
A window is valid if we can replace at most `k` characters to make all characters in the window identical. This is true if `window_size - max_freq_char_count <= k`.
1. We track the frequency of characters in the window and the highest frequency (`max_count`).
2. If the current window becomes invalid, we shrink it from the left.
3. Interestingly, `max_count` only needs to be updated when it increases, because a smaller `max_count` won't allow for a larger valid window than what we've already found.

```python
def character_replacement(s: str, k: int) -> int:
    """
    Longest substring with same letter after replacing at most k chars.

    Time Complexity: Θ(n). Single pass with the right pointer, and left pointer
                     moves at most n times.
    Space Complexity: O(1). The hash map stores at most 26 uppercase English letters,
                      making it O(1) space. Dictionary updates are amortized O(1).

    Example:
    s = "AABABBA", k = 1 → 4 ("AABA" → "AAAA")
    """
    count: dict[str, int] = {}
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

### Problem: Subarray Sum Equals K
**Problem Statement:** Given an array of integers `nums` and an integer `k`, return the total number of subarrays whose sum equals to `k`.

**Why it works:**
This problem uses Prefix Sum because the array can contain negative numbers, which breaks the monotonic property required for sliding window.
1. If the sum of elements from index `0` to `j` is `P_j` and from `0` to `i-1` is `P_{i-1}`, then the sum from `i` to `j` is `P_j - P_{i-1}`.
2. We want `P_j - P_{i-1} = k`, which means `P_{i-1} = P_j - k`.
3. As we compute prefix sums, we store their frequencies in a hash map. At each index `j`, we check how many times `P_j - k` has occurred as a prefix sum before.

```python
def subarray_sum(nums: list[int], k: int) -> int:
    """
    Count subarrays with sum equal to k.

    Note: This is NOT sliding window (handles negatives).
    Uses prefix sum with hashmap.

    Time Complexity: O(n). A single pass through the array. Note that we rely
                     on Python's dictionary, which has amortized O(1) lookups
                     but worst-case O(n) lookups if hash collisions occur.
    Space Complexity: O(n). The hash map stores at most n + 1 distinct prefix
                      sums in the worst-case.

    Example:
    nums = [1, 1, 1], k = 2 → 2
    """
    count = 0
    prefix_sum = 0
    prefix_count: dict[int, int] = {0: 1}  # prefix_sum → count

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

### Problem: Minimum Size Subarray Sum
**Problem Statement:** Given an array of positive integers `nums` and a positive integer `target`, return the minimal length of a contiguous subarray of which the sum is greater than or equal to `target`. If there is no such subarray, return 0 instead.

**Why it works:**
Since all numbers are positive, the window sum is monotonic (adding elements increases it, removing decreases it).
1. **Expand**: Move `right` until the `current_sum >= target`.
2. **Shrink**: Once the condition is met, move `left` to minimize the window while the condition still holds.
3. This "greedy" shrinkage finds the smallest subarray ending at `right` that satisfies the target.

```python
def min_subarray_len(target: int, nums: list[int]) -> int:
    """
    Minimum length subarray with sum >= target.
    All positive numbers.

    Time Complexity: Θ(n). Right pointer moves n times. The inner while loop
                     moves the left pointer at most n times across all iterations.
    Space Complexity: O(1). Only scalar variables. Note: `nums` is a Python
                      list (dynamic array), but no auxiliary data structures are used.

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
from typing import Callable, Any

def sliding_window_variable(arr: list[Any], condition_func: Callable[[Any], bool]) -> int:
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
    window_state: dict[Any, Any] = {}  # whatever state you need

    # Note: 'arr' could be a dynamic array (Python list) or a string.
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
