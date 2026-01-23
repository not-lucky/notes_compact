# Sliding Window: Fixed Size

## Practice Problems

### 1. Maximum Sum Subarray of Size K
**Difficulty:** Easy
**Key Technique:** Basic sliding sum

```python
def max_sum_subarray(nums: list[int], k: int) -> int:
    """
    Finds maximum sum of any contiguous subarray of size k.
    Time: O(n)
    Space: O(1)
    """
    if not nums or k <= 0: return 0
    curr_sum = sum(nums[:k])
    max_sum = curr_sum
    for i in range(k, len(nums)):
        curr_sum += nums[i] - nums[i - k]
        max_sum = max(max_sum, curr_sum)
    return max_sum
```

### 2. Maximum Average Subarray I
**Difficulty:** Easy
**Key Technique:** Sum -> average

```python
def find_max_average(nums: list[int], k: int) -> float:
    """
    Finds contiguous subarray of length k with maximum average.
    Time: O(n)
    Space: O(1)
    """
    curr_sum = sum(nums[:k])
    max_sum = curr_sum
    for i in range(k, len(nums)):
        curr_sum += nums[i] - nums[i - k]
        max_sum = max(max_sum, curr_sum)
    return max_sum / k
```

### 3. Find All Anagrams in a String
**Difficulty:** Medium
**Key Technique:** Frequency matching

```python
from collections import Counter

def find_anagrams(s: str, p: str) -> list[int]:
    """
    Finds all starting indices of p's anagrams in s.
    Time: O(n)
    Space: O(1) (max 26 chars)
    """
    if len(p) > len(s): return []
    p_count = Counter(p)
    s_count = Counter(s[:len(p)])
    res = []
    if s_count == p_count: res.append(0)

    k = len(p)
    for i in range(k, len(s)):
        s_count[s[i]] += 1
        s_count[s[i - k]] -= 1
        if s_count[s[i - k]] == 0:
            del s_count[s[i - k]]
        if s_count == p_count:
            res.append(i - k + 1)
    return res
```

### 4. Permutation in String
**Difficulty:** Medium
**Key Technique:** Same as anagrams

```python
def check_inclusion(p: str, s: str) -> bool:
    """
    Returns true if s contains a permutation of p.
    Time: O(n)
    Space: O(1)
    """
    if len(p) > len(s): return False
    p_cnt, s_cnt = [0]*26, [0]*26
    for i in range(len(p)):
        p_cnt[ord(p[i]) - ord('a')] += 1
        s_cnt[ord(s[i]) - ord('a')] += 1

    if p_cnt == s_cnt: return True

    for i in range(len(p), len(s)):
        s_cnt[ord(s[i]) - ord('a')] += 1
        s_cnt[ord(s[i - len(p)]) - ord('a')] -= 1
        if p_cnt == s_cnt: return True
    return False
```

### 5. Sliding Window Maximum
**Difficulty:** Hard
**Key Technique:** Monotonic deque

```python
from collections import deque

def max_sliding_window(nums: list[int], k: int) -> list[int]:
    """
    Finds maximum for each sliding window of size k.
    Time: O(n)
    Space: O(k)
    """
    dq = deque()
    res = []
    for i, num in enumerate(nums):
        while dq and nums[dq[-1]] < num:
            dq.pop()
        dq.append(i)
        if dq[0] == i - k:
            dq.popleft()
        if i >= k - 1:
            res.append(nums[dq[0]])
    return res
```

### 6. Contains Duplicate II
**Difficulty:** Easy
**Key Technique:** HashSet window

```python
def contains_nearby_duplicate(nums: list[int], k: int) -> bool:
    """
    Checks if same value exists within distance k.
    Time: O(n)
    Space: O(k)
    """
    seen = set()
    for i, num in enumerate(nums):
        if num in seen: return True
        seen.add(num)
        if len(seen) > k:
            seen.remove(nums[i - k])
    return False
```

### 7. Repeated DNA Sequences
**Difficulty:** Medium
**Key Technique:** Hash of window

```python
def find_repeated_dna_sequences(s: str) -> list[str]:
    """
    Finds all 10-letter sequences that occur more than once.
    Time: O(n)
    Space: O(n)
    """
    seen, res = set(), set()
    for i in range(len(s) - 9):
        ten = s[i:i+10]
        if ten in seen:
            res.add(ten)
        seen.add(ten)
    return list(res)
```
