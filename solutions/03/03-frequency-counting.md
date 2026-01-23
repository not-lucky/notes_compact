# Frequency Counting

## Practice Problems

### 1. Top K Frequent Elements
**Difficulty:** Medium
**Key Technique:** Counter + Bucket Sort (or Heap)

```python
from collections import Counter

def top_k_frequent(nums: list[int], k: int) -> list[int]:
    """
    Time: O(n)
    Space: O(n)
    """
    count = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]
    for num, freq in count.items():
        buckets[freq].append(num)

    res = []
    for i in range(len(buckets) - 1, 0, -1):
        for num in buckets[i]:
            res.append(num)
            if len(res) == k:
                return res
```

### 2. Top K Frequent Words
**Difficulty:** Medium
**Key Technique:** Counter + Heap with custom comparator

```python
import heapq
from collections import Counter

def top_k_frequent_words(words: list[str], k: int) -> list[str]:
    """
    Time: O(n log k)
    Space: O(n)
    """
    cnt = Counter(words)
    # Use negative frequency for max-heap behavior with word for tie-break
    heap = [(-freq, word) for word, freq in cnt.items()]
    heapq.heapify(heap)
    return [heapq.heappop(heap)[1] for _ in range(k)]
```

### 3. Majority Element
**Difficulty:** Easy
**Key Technique:** Boyer-Moore Voting Algorithm

```python
def majority_element(nums: list[int]) -> int:
    """
    Time: O(n)
    Space: O(1)
    """
    candidate = None
    count = 0
    for n in nums:
        if count == 0:
            candidate = n
        count += (1 if n == candidate else -1)
    return candidate
```

### 4. Majority Element II
**Difficulty:** Medium
**Key Technique:** Boyer-Moore for 2 candidates

```python
def majority_element_ii(nums: list[int]) -> list[int]:
    """
    Find all elements appearing more than n/3 times.
    Time: O(n)
    Space: O(1)
    """
    c1, c2, cnt1, cnt2 = None, None, 0, 0
    for n in nums:
        if n == c1: cnt1 += 1
        elif n == c2: cnt2 += 1
        elif cnt1 == 0: c1, cnt1 = n, 1
        elif cnt2 == 0: c2, cnt2 = n, 1
        else:
            cnt1 -= 1
            cnt2 -= 1

    res = []
    for c in [c1, c2]:
        if c is not None and nums.count(c) > len(nums) // 3:
            res.append(c)
    return res
```

### 5. First Unique Character in a String
**Difficulty:** Easy
**Key Technique:** Frequency counting

```python
from collections import Counter

def first_uniq_char(s: str) -> int:
    """
    Time: O(n)
    Space: O(1) (26 chars)
    """
    count = Counter(s)
    for i, char in enumerate(s):
        if count[char] == 1:
            return i
    return -1
```

### 6. Single Number
**Difficulty:** Easy
**Key Technique:** XOR

```python
def single_number(nums: list[int]) -> int:
    """
    Time: O(n)
    Space: O(1)
    """
    res = 0
    for n in nums:
        res ^= n
    return res
```

### 7. Contains Duplicate
**Difficulty:** Easy
**Key Technique:** Set

```python
def contains_duplicate(nums: list[int]) -> bool:
    """
    Time: O(n)
    Space: O(n)
    """
    return len(set(nums)) < len(nums)
```

### 8. Contains Duplicate II
**Difficulty:** Easy
**Key Technique:** Sliding window set or Hashmap

```python
def contains_nearby_duplicate(nums: list[int], k: int) -> bool:
    """
    Time: O(n)
    Space: O(min(n, k))
    """
    window = set()
    for i, n in enumerate(nums):
        if n in window: return True
        window.add(n)
        if len(window) > k:
            window.remove(nums[i-k])
    return False
```
