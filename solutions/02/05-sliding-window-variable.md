# Sliding Window: Variable Size

## Practice Problems

### 1. Longest Substring Without Repeating Characters
**Difficulty:** Medium
**Pattern:** Set/Map window

```python
def length_of_longest_substring(s: str) -> int:
    """
    Time: O(n)
    Space: O(k) where k is size of charset
    """
    seen = {}
    l = 0
    res = 0
    for r, char in enumerate(s):
        if char in seen and seen[char] >= l:
            l = seen[char] + 1
        seen[char] = r
        res = max(res, r - l + 1)
    return res
```

### 2. Minimum Window Substring
**Difficulty:** Hard
**Pattern:** Character matching

```python
from collections import Counter

def min_window(s: str, t: str) -> str:
    """
    Time: O(n + m)
    Space: O(m)
    """
    if not t or not s: return ""
    t_count = Counter(t)
    window = {}
    have, need = 0, len(t_count)
    res, res_len = [-1, -1], float('inf')
    l = 0
    for r, char in enumerate(s):
        window[char] = window.get(char, 0) + 1
        if char in t_count and window[char] == t_count[char]:
            have += 1

        while have == need:
            if (r - l + 1) < res_len:
                res = [l, r]
                res_len = r - l + 1
            window[s[l]] -= 1
            if s[l] in t_count and window[s[l]] < t_count[s[l]]:
                have -= 1
            l += 1
    l, r = res
    return s[l:r+1] if res_len != float('inf') else ""
```

### 3. Longest Substring with At Most K Distinct
**Difficulty:** Medium
**Pattern:** Counter window

```python
def length_of_longest_substring_k_distinct(s: str, k: int) -> int:
    """
    Time: O(n)
    Space: O(k)
    """
    if k == 0: return 0
    counts = {}
    l = 0
    res = 0
    for r, char in enumerate(s):
        counts[char] = counts.get(char, 0) + 1
        while len(counts) > k:
            counts[s[l]] -= 1
            if counts[s[l]] == 0:
                del counts[s[l]]
            l += 1
        res = max(res, r - l + 1)
    return res
```

### 4. Longest Repeating Character Replacement
**Difficulty:** Medium
**Pattern:** Max count tracking

```python
def character_replacement(s: str, k: int) -> int:
    """
    Time: O(n)
    Space: O(26)
    """
    counts = {}
    l = 0
    max_f = 0
    res = 0
    for r, char in enumerate(s):
        counts[char] = counts.get(char, 0) + 1
        max_f = max(max_f, counts[char])
        while (r - l + 1) - max_f > k:
            counts[s[l]] -= 1
            l += 1
        res = max(res, r - l + 1)
    return res
```

### 5. Fruit Into Baskets
**Difficulty:** Medium
**Pattern:** At most 2 distinct

```python
def total_fruit(fruits: list[int]) -> int:
    """
    Time: O(n)
    Space: O(1) (at most 3 types in map)
    """
    counts = {}
    l = 0
    res = 0
    for r, f in enumerate(fruits):
        counts[f] = counts.get(f, 0) + 1
        while len(counts) > 2:
            counts[fruits[l]] -= 1
            if counts[fruits[l]] == 0:
                del counts[fruits[l]]
            l += 1
        res = max(res, r - l + 1)
    return res
```

### 6. Subarray Product Less Than K
**Difficulty:** Medium
**Pattern:** Product window

```python
def num_subarray_product_less_than_k(nums: list[int], k: int) -> int:
    """
    Time: O(n)
    Space: O(1)
    """
    if k <= 1: return 0
    l = 0
    prod = 1
    res = 0
    for r, num in enumerate(nums):
        prod *= num
        while prod >= k:
            prod //= nums[l]
            l += 1
        res += r - l + 1
    return res
```

### 7. Minimum Size Subarray Sum
**Difficulty:** Medium
**Pattern:** Sum >= target

```python
def min_sub_array_len(target: int, nums: list[int]) -> int:
    """
    Time: O(n)
    Space: O(1)
    """
    l = 0
    curr_sum = 0
    res = float('inf')
    for r, num in enumerate(nums):
        curr_sum += num
        while curr_sum >= target:
            res = min(res, r - l + 1)
            curr_sum -= nums[l]
            l += 1
    return res if res != float('inf') else 0
```

### 8. Maximum Erasure Value
**Difficulty:** Medium
**Pattern:** Unique elements sum

```python
def maximum_unique_subarray(nums: list[int]) -> int:
    """
    Time: O(n)
    Space: O(n)
    """
    seen = set()
    l = 0
    curr_sum = 0
    res = 0
    for r, num in enumerate(nums):
        while num in seen:
            seen.remove(nums[l])
            curr_sum -= nums[l]
            l += 1
        seen.add(num)
        curr_sum += num
        res = max(res, curr_sum)
    return res
```
