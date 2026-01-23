# Set Operations

## Practice Problems

### 1. Intersection of Two Arrays
**Difficulty:** Easy
**Key Technique:** Set intersection

```python
def intersection(nums1: list[int], nums2: list[int]) -> list[int]:
    """
    Time: O(n + m)
    Space: O(n + m)
    """
    return list(set(nums1) & set(nums2))
```

### 2. Intersection of Two Arrays II
**Difficulty:** Easy
**Key Technique:** Counter

```python
from collections import Counter

def intersect(nums1: list[int], nums2: list[int]) -> list[int]:
    """
    Time: O(n + m)
    Space: O(min(n, m))
    """
    c1 = Counter(nums1)
    res = []
    for n in nums2:
        if c1[n] > 0:
            res.append(n)
            c1[n] -= 1
    return res
```

### 3. Happy Number
**Difficulty:** Easy
**Key Technique:** Set for cycle detection

```python
def is_happy(n: int) -> bool:
    """
    Time: O(log n)
    Space: O(log n)
    """
    def get_next(num):
        total = 0
        while num > 0:
            num, digit = divmod(num, 10)
            total += digit ** 2
        return total

    seen = set()
    while n != 1 and n not in seen:
        seen.add(n)
        n = get_next(n)
    return n == 1
```

### 4. Longest Consecutive Sequence
**Difficulty:** Medium
**Key Technique:** Set + sequence start check

```python
def longest_consecutive(nums: list[int]) -> int:
    """
    Time: O(n)
    Space: O(n)
    """
    num_set = set(nums)
    res = 0
    for n in num_set:
        if n - 1 not in num_set:
            curr = n
            curr_len = 1
            while curr + 1 in num_set:
                curr += 1
                curr_len += 1
            res = max(res, curr_len)
    return res
```

### 5. Missing Number
**Difficulty:** Easy
**Key Technique:** Sum or XOR

```python
def missing_number(nums: list[int]) -> int:
    """
    Time: O(n)
    Space: O(1)
    """
    n = len(nums)
    return n * (n + 1) // 2 - sum(nums)
```

### 6. Find All Numbers Disappeared in an Array
**Difficulty:** Easy
**Key Technique:** Index marking (array as set)

```python
def find_disappeared_numbers(nums: list[int]) -> list[int]:
    """
    Time: O(n)
    Space: O(1)
    """
    for n in nums:
        idx = abs(n) - 1
        nums[idx] = -abs(nums[idx])
    return [i + 1 for i, n in enumerate(nums) if n > 0]
```

### 7. Isomorphic Strings
**Difficulty:** Easy
**Key Technique:** Bidirectional mapping

```python
def is_isomorphic(s: str, t: str) -> bool:
    """
    Time: O(n)
    Space: O(min(n, 26))
    """
    s2t, t2s = {}, {}
    for c1, c2 in zip(s, t):
        if (c1 in s2t and s2t[c1] != c2) or (c2 in t2s and t2s[c2] != c1):
            return False
        s2t[c1] = c2
        t2s[c2] = c1
    return True
```

### 8. Word Pattern
**Difficulty:** Easy
**Key Technique:** Bidirectional mapping

```python
def word_pattern(pattern: str, s: str) -> bool:
    """
    Time: O(n)
    Space: O(n)
    """
    words = s.split()
    if len(pattern) != len(words): return False
    p2w, w2p = {}, {}
    for p, w in zip(pattern, words):
        if (p in p2w and p2w[p] != w) or (w in w2p and w2p[w] != p):
            return False
        p2w[p] = w
        w2p[w] = p
    return True
```
