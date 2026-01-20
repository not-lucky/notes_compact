# Longest Substring Without Repeating Characters

## Problem Statement

Given a string `s`, find the length of the longest substring without repeating characters.

**Example:**
```
Input: s = "abcabcbb"
Output: 3
Explanation: "abc" is the longest substring without repeating characters.

Input: s = "bbbbb"
Output: 1

Input: s = "pwwkew"
Output: 3
Explanation: "wke" is the answer (not "pwke" - must be contiguous substring).
```

## Building Intuition

### Why This Works

The sliding window maintains an invariant: all characters in the window `[left, right]` are unique. We expand `right` to explore new characters. When we encounter a character that already exists in the window, we shrink from `left` until the duplicate is removed.

The hash map optimization stores the last index where each character was seen. When we find a duplicate, instead of incrementing `left` one by one, we can jump `left` directly to one past the previous occurrence of the duplicate character. This ensures each character is processed at most twice (once when entering the window, once when determining where to jump `left`).

The window never shrinks unnecessarily. We only shrink when forced to by a duplicate, and we shrink exactly as much as needed. This greedy expansion, minimal shrinkage strategy is optimal.

### How to Discover This

Sliding window is the go-to technique for "longest/shortest contiguous substring/subarray satisfying some property." The property here is "all unique characters."

Think in terms of the invariant: what must be true about the window? How do we restore the invariant when it is violated? Here, the invariant is uniqueness; violation is a duplicate; restoration is shrinking until the duplicate is gone.

### Pattern Recognition

This is the **Sliding Window with Invariant** pattern. It appears in:
- Longest substring without repeating (this problem)
- Longest substring with at most k distinct characters
- Minimum window substring
- Longest repeating character replacement
- Any problem asking for optimal contiguous segment with a constraint

## When NOT to Use

- **When the constraint is not about contiguity**: Sliding window only works for contiguous substrings/subarrays. For subsequences, you need DP or other techniques.
- **When the invariant cannot be restored monotonically**: Sliding window assumes that shrinking the window from one side can restore the invariant. If violations require more complex repairs, the technique breaks down.
- **When you need all qualifying substrings, not just the longest**: Sliding window finds the optimal one. Enumerating all requires different approaches.
- **When the "window" is not a simple range**: If valid substrings can have gaps or complex structure, sliding window does not apply.

## Approach

### Sliding Window with Hash Set
Maintain a window `[left, right]` where all characters are unique.
- Expand `right` to include new characters
- When duplicate found, shrink from `left` until duplicate removed

### Optimized: Hash Map with Index
Store the last seen index of each character. When duplicate found, jump `left` directly to after the previous occurrence.

```
s = "abcabcbb"

Step 1: a → window="a", seen={a:0}, max=1
Step 2: b → window="ab", seen={a:0,b:1}, max=2
Step 3: c → window="abc", seen={a:0,b:1,c:2}, max=3
Step 4: a → duplicate! left jumps to 1, window="bca", seen={a:3,b:1,c:2}, max=3
Step 5: b → duplicate! left jumps to 2, window="cab", seen={a:3,b:4,c:2}, max=3
...
```

## Implementation

```python
def length_of_longest_substring(s: str) -> int:
    """
    Find longest substring without repeating characters.

    Time: O(n) - each character visited at most twice
    Space: O(min(m, n)) - m is charset size, n is string length
    """
    char_index = {}  # character -> last seen index
    max_length = 0
    left = 0

    for right, char in enumerate(s):
        # If char seen before and within current window
        if char in char_index and char_index[char] >= left:
            left = char_index[char] + 1

        char_index[char] = right
        max_length = max(max_length, right - left + 1)

    return max_length


def length_of_longest_substring_set(s: str) -> int:
    """
    Using hash set (more intuitive, slightly slower).

    Time: O(n) - each char added/removed at most once
    Space: O(min(m, n))
    """
    char_set = set()
    max_length = 0
    left = 0

    for right, char in enumerate(s):
        # Shrink window until char can be added
        while char in char_set:
            char_set.remove(s[left])
            left += 1

        char_set.add(char)
        max_length = max(max_length, right - left + 1)

    return max_length


def length_of_longest_substring_array(s: str) -> int:
    """
    Using array for ASCII characters (fastest).

    Time: O(n)
    Space: O(128) = O(1) for ASCII
    """
    last_seen = [-1] * 128  # ASCII characters
    max_length = 0
    left = 0

    for right, char in enumerate(s):
        idx = ord(char)
        if last_seen[idx] >= left:
            left = last_seen[idx] + 1
        last_seen[idx] = right
        max_length = max(max_length, right - left + 1)

    return max_length
```

## Complexity Analysis

| Method | Time | Space | Notes |
|--------|------|-------|-------|
| Hash Map | O(n) | O(min(m,n)) | m = charset size |
| Hash Set | O(n) | O(min(m,n)) | May have more operations |
| Array | O(n) | O(128) | Fastest for ASCII |

## Edge Cases

1. **Empty string**: Return 0
2. **Single character**: Return 1
3. **All same characters**: `"aaaa"` → 1
4. **All unique characters**: `"abcd"` → length of string
5. **Unicode characters**: Use hash map, not array
6. **Spaces and special characters**: Treated as regular characters

## Common Mistakes

1. **Not updating left correctly**: Must be `max(left, char_index[char] + 1)` or check if within window
2. **Off-by-one in length calculation**: Length is `right - left + 1`
3. **Forgetting to update character index**: Always update even when no duplicate
4. **Using wrong data structure**: Array only works for limited charset

## Visual Walkthrough

```
s = "abcabcbb"

Window evolution:
[a] b c a b c b b    max=1
[a b] c a b c b b    max=2
[a b c] a b c b b    max=3
 a [b c a] b c b b   max=3 (a repeated, left jumps)
 a b [c a b] c b b   max=3 (b repeated, left jumps)
 a b c [a b c] b b   max=3 (c repeated, left jumps)
 a b c a [b c b] b   max=3 (b repeated, left jumps)
 a b c a b [c b] b   max=3
 a b c a b c [b] b   max=3 (b repeated, left jumps)
 a b c a b c b [b]   max=3

Result: 3
```

## Variations

### Longest Substring with At Most K Distinct Characters
```python
def longest_substring_k_distinct(s: str, k: int) -> int:
    """
    At most k distinct characters allowed.
    """
    from collections import defaultdict

    char_count = defaultdict(int)
    max_length = 0
    left = 0

    for right, char in enumerate(s):
        char_count[char] += 1

        while len(char_count) > k:
            char_count[s[left]] -= 1
            if char_count[s[left]] == 0:
                del char_count[s[left]]
            left += 1

        max_length = max(max_length, right - left + 1)

    return max_length
```

### Longest Substring with At Most Two Distinct Characters
Same as above with `k=2`.

### Longest Repeating Character Replacement
```python
def character_replacement(s: str, k: int) -> int:
    """
    Replace at most k characters to get longest repeating substring.
    """
    count = {}
    max_count = 0  # Count of most frequent char in window
    max_length = 0
    left = 0

    for right, char in enumerate(s):
        count[char] = count.get(char, 0) + 1
        max_count = max(max_count, count[char])

        # Window is valid if we can replace all others
        # (window_size - max_count) <= k
        while (right - left + 1) - max_count > k:
            count[s[left]] -= 1
            left += 1

        max_length = max(max_length, right - left + 1)

    return max_length
```

## Related Problems

- **Minimum Window Substring** - Find smallest window containing all chars
- **Longest Substring with At Most K Distinct Characters**
- **Longest Repeating Character Replacement**
- **Substring with Concatenation of All Words**
- **Permutation in String** - Check if permutation exists as substring
