# Sliding Window: Variable Size - Solutions

## Practice Problems

### 1. Longest Substring Without Repeating Characters

**Problem Statement**: Given a string `s`, find the length of the longest substring without repeating characters.

**Examples & Edge Cases**:

- Example: `"abcabcbb"` -> `3` (`"abc"`)
- Edge Case: Empty string.
- Edge Case: String with all same characters.

**Optimal Python Solution**:

```python
def lengthOfLongestSubstring(s: str) -> int:
    # char_map stores the last seen index of each character
    char_map = {}
    left = 0
    max_len = 0

    for right in range(len(s)):
        # If character is in current window, move left pointer
        if s[right] in char_map and char_map[s[right]] >= left:
            left = char_map[s[right]] + 1

        # Update last seen index
        char_map[s[right]] = right
        # Update max length
        max_len = max(max_len, right - left + 1)

    return max_len
```

**Explanation**:
We use a sliding window defined by `left` and `right`. As we move `right`, we keep track of the last seen index of each character in a hash map. If we encounter a character that is already in our current window, we move the `left` pointer to the position after its last occurrence.

**Complexity Analysis**:

- **Time Complexity**: O(n), where n is the length of the string. We iterate through the string once.
- **Space Complexity**: O(min(n, m)), where m is the size of the character set (e.g., 26 for letters, or 128/256 for ASCII).

---

### 2. Minimum Window Substring

**Problem Statement**: Given two strings `s` and `t`, return the minimum window substring of `s` such that every character in `t` (including duplicates) is included in the window.

**Optimal Python Solution**:

```python
from collections import Counter

def minWindow(s: str, t: str) -> str:
    if not t or not s:
        return ""

    dict_t = Counter(t)
    required = len(dict_t)

    # left and right pointers
    l, r = 0, 0
    # formed is used to keep track of how many unique characters in t are present in the window
    formed = 0
    window_counts = {}

    # ans tuple of (window length, left, right)
    ans = float("inf"), None, None

    while r < len(s):
        character = s[r]
        window_counts[character] = window_counts.get(character, 0) + 1

        if character in dict_t and window_counts[character] == dict_t[character]:
            formed += 1

        # Try and contract the window till the point where it ceases to be 'desirable'
        while l <= r and formed == required:
            character = s[l]

            # Save the smallest window until now
            if r - l + 1 < ans[0]:
                ans = (r - l + 1, l, r)

            window_counts[character] -= 1
            if character in dict_t and window_counts[character] < dict_t[character]:
                formed -= 1

            l += 1

        r += 1

    return "" if ans[0] == float("inf") else s[ans[1] : ans[2] + 1]
```

**Explanation**:
We expand the window using the `r` pointer until all characters of `t` are present. Then we shrink the window from the `l` pointer as much as possible while maintaining the property that all characters of `t` are still in the window. We track the smallest window seen so far.

**Complexity Analysis**:

- **Time Complexity**: O(n + m), where n is length of `s` and m is length of `t`.
- **Space Complexity**: O(n + m).

---

### 3. Longest Substring with At Most K Distinct Characters

**Problem Statement**: Given a string `s` and an integer `k`, return the length of the longest substring of `s` that contains at most `k` distinct characters.

**Optimal Python Solution**:

```python
from collections import Counter

def lengthOfLongestSubstringKDistinct(s: str, k: int) -> int:
    if k == 0:
        return 0

    left = 0
    max_len = 0
    counts = Counter()

    for right in range(len(s)):
        counts[s[right]] += 1

        # While we have more than k distinct characters, shrink from left
        while len(counts) > k:
            counts[s[left]] -= 1
            if counts[s[left]] == 0:
                del counts[s[left]]
            left += 1

        max_len = max(max_len, right - left + 1)

    return max_len
```

**Explanation**:
We use a frequency map to keep track of distinct characters and their counts in the current window. If the number of distinct characters exceeds `k`, we move the `left` pointer until we remove a character completely from the map.

**Complexity Analysis**:

- **Time Complexity**: O(n).
- **Space Complexity**: O(k) for the frequency map.

---

### 4. Longest Repeating Character Replacement

**Problem Statement**: You are given a string `s` and an integer `k`. You can choose any character of the string and change it to any other uppercase English character. You can perform this operation at most `k` times. Return the length of the longest substring containing the same letter you can get after performing the above operations.

**Optimal Python Solution**:

```python
def characterReplacement(s: str, k: int) -> int:
    count = {}
    max_f = 0
    left = 0
    res = 0

    for right in range(len(s)):
        count[s[right]] = count.get(s[right], 0) + 1
        max_f = max(max_f, count[s[right]])

        # Window size - max frequency = number of characters to replace
        while (right - left + 1) - max_f > k:
            count[s[left]] -= 1
            left += 1

        res = max(res, right - left + 1)
    return res
```

**Explanation**:
A window is valid if we can turn all characters into the most frequent character using at most `k` operations. The number of operations needed is `window_length - max_frequency`. We maintain this property by shrinking `left` whenever it's violated.

**Complexity Analysis**:

- **Time Complexity**: O(n).
- **Space Complexity**: O(26) = O(1).

---

### 5. Fruit Into Baskets

**Problem Statement**: You are visiting a farm that has a single row of fruit trees from left to right. You have two baskets, and each basket can only hold a single type of fruit. There is no limit on the amount of fruit each basket can hold. You want to collect as much fruit as possible. Starting from any tree of your choice, you must pick exactly one fruit from every tree while moving to the right. The process stops when you reach a tree with fruit that cannot fit in your baskets.

**Optimal Python Solution**:

```python
from collections import Counter

def totalFruit(fruits: list[int]) -> int:
    # This is equivalent to "Longest Subarray with at most 2 distinct elements"
    counts = Counter()
    left = 0
    max_fruits = 0

    for right in range(len(fruits)):
        counts[fruits[right]] += 1

        while len(counts) > 2:
            counts[fruits[left]] -= 1
            if counts[fruits[left]] == 0:
                del counts[fruits[left]]
            left += 1

        max_fruits = max(max_fruits, right - left + 1)

    return max_fruits
```

**Explanation**:
The problem translates to finding the longest contiguous subarray containing at most two unique numbers. We use a sliding window and a frequency map to enforce this constraint.

**Complexity Analysis**:

- **Time Complexity**: O(n).
- **Space Complexity**: O(1) (maximum 3 keys in Counter).

---

### 6. Subarray Product Less Than K

**Problem Statement**: Given an array of integers `nums` and an integer `k`, return the number of contiguous subarrays where the product of all the elements in the subarray is strictly less than `k`.

**Optimal Python Solution**:

```python
def numSubarrayProductLessThanK(nums: list[int], k: int) -> int:
    if k <= 1:
        return 0

    prod = 1
    left = 0
    count = 0

    for right in range(len(nums)):
        prod *= nums[right]

        while prod >= k:
            prod /= nums[left]
            left += 1

        # Number of subarrays ending at right: [left, right], [left+1, right], ..., [right, right]
        count += right - left + 1

    return count
```

**Explanation**:
As we expand the `right` pointer, we update the product. If the product becomes too large, we shrink the `left` pointer. For every valid window `[left, right]`, all subarrays starting from any index between `left` and `right` and ending at `right` are also valid. There are `right - left + 1` such subarrays.

**Complexity Analysis**:

- **Time Complexity**: O(n).
- **Space Complexity**: O(1).

---

### 7. Minimum Size Subarray Sum

**Problem Statement**: Given an array of positive integers `nums` and a positive integer `target`, return the minimal length of a contiguous subarray of which the sum is greater than or equal to `target`. If there is no such subarray, return 0 instead.

**Optimal Python Solution**:

```python
def minSubArrayLen(target: int, nums: list[int]) -> int:
    left = 0
    current_sum = 0
    min_len = float('inf')

    for right in range(len(nums)):
        current_sum += nums[right]

        while current_sum >= target:
            min_len = min(min_len, right - left + 1)
            current_sum -= nums[left]
            left += 1

    return min_len if min_len != float('inf') else 0
```

**Explanation**:
We expand the window until the sum reaches the target. Then, we try to shrink the window from the left as much as possible while still maintaining a sum $\ge$ target, tracking the minimum length found.

**Complexity Analysis**:

- **Time Complexity**: O(n).
- **Space Complexity**: O(1).

---

### 8. Maximum Erasure Value

**Problem Statement**: You are given an array of positive integers `nums` and want to erase a subarray containing unique elements. The score you get by erasing the subarray is equal to the sum of its elements. Return the maximum score you can get by erasing exactly one subarray.

**Optimal Python Solution**:

```python
def maximumUniqueSubarray(nums: list[int]) -> int:
    seen = set()
    current_sum = 0
    max_sum = 0
    left = 0

    for right in range(len(nums)):
        # While the current element is a duplicate, shrink from left
        while nums[right] in seen:
            seen.remove(nums[left])
            current_sum -= nums[left]
            left += 1

        seen.add(nums[right])
        current_sum += nums[right]
        max_sum = max(max_sum, current_sum)

    return max_sum
```

**Explanation**:
We use a sliding window to find subarrays with all unique elements. We use a set to track elements in the current window and a running sum to compute the score. If we hit a duplicate, we shrink from the left until the duplicate is removed.

**Complexity Analysis**:

- **Time Complexity**: O(n).
- **Space Complexity**: O(n) in worst case for the set.
