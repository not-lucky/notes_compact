# Frequency Counting - Solutions

## 1. Top K Frequent Elements

Given an integer array `nums` and an integer `k`, return the `k` most frequent elements. You may return the answer in any order.

### Problem Statement

Identify which elements in an array appear most often.

### Examples & Edge Cases

**Example 1:**

- Input: `nums = [1, 1, 1, 2, 2, 3], k = 2`
- Output: `[1, 2]`

**Example 2:**

- Input: `nums = [1], k = 1`
- Output: `[1]`

**Edge Cases:**

- `k` is equal to the number of unique elements.
- Array has all unique elements (any `k` elements are valid).
- Multiple elements have the same frequency.

### Optimal Python Solution (Bucket Sort - O(n))

```python
from collections import Counter

def topKFrequent(nums: list[int], k: int) -> list[int]:
    """
    Use Bucket Sort for O(n) time.
    1. Count frequencies.
    2. Create buckets where index is the frequency.
    3. Iterate backwards from highest frequency bucket.
    """
    # 1. Count frequencies: O(n)
    counts = Counter(nums)

    # 2. Group numbers by frequency: O(n)
    # buckets[f] contains a list of numbers that appear f times
    n = len(nums)
    buckets = [[] for _ in range(n + 1)]
    for num, freq in counts.items():
        buckets[freq].append(num)

    # 3. Collect the top k elements: O(n)
    result = []
    # Iterate from the highest possible frequency (n) down to 1
    for freq in range(n, 0, -1):
        for num in buckets[freq]:
            result.append(num)
            if len(result) == k:
                return result

    return result
```

### Explanation

1.  **Counting**: We use `Counter` to get the frequency of each number.
2.  **Bucketing**: Instead of sorting the frequencies (which would take O(n log n)), we use the fact that the maximum possible frequency is `n` (the size of the array). We create an array of lists called `buckets`. If a number `X` appears `f` times, we put `X` into `buckets[f]`.
3.  **Collection**: We iterate through the `buckets` starting from the end (highest frequency). We pull numbers out of the buckets until we have collected `k` elements.

### Complexity Analysis

- **Time Complexity**: O(n). We traverse `nums` to count, then we iterate over unique elements to fill buckets, then we traverse buckets. All these steps are linear relative to `n`.
- **Space Complexity**: O(n). We store the frequency map and the bucket array, both of which take O(n) space in the worst case.

---

## 2. Top K Frequent Words

Given an array of strings `words` and an integer `k`, return the `k` most frequent strings. Return the answer sorted by the frequency from highest to lowest. Sort the words with the same frequency by their lexicographical order.

### Optimal Python Solution (Heap - O(n log k))

```python
import heapq
from collections import Counter

class Word:
    def __init__(self, word, freq):
        self.word = word
        self.freq = freq

    def __lt__(self, other):
        # We want higher frequency at the bottom of the min-heap
        if self.freq == other.freq:
            # For same frequency, we want lexicographically larger word at top
            # so that it gets popped out first in a min-heap,
            # leaving the lexicographically smaller ones.
            return self.word > other.word
        return self.freq < other.freq

def topKFrequentWords(words: list[str], k: int) -> list[str]:
    counts = Counter(words)
    heap = []

    for word, freq in counts.items():
        heapq.heappush(heap, Word(word, freq))
        if len(heap) > k:
            heapq.heappop(heap)

    # Pop remaining elements and reverse to get highest freq first
    res = []
    while heap:
        res.append(heapq.heappop(heap).word)
    return res[::-1]
```

### Complexity Analysis

- **Time Complexity**: O(n log k). We process `n` elements, and each heap operation is O(log k).
- **Space Complexity**: O(n) for the frequency map.

---

## 3. Majority Element

Given an array `nums` of size `n`, return the majority element. The majority element is the element that appears more than `⌊n / 2⌋` times.

### Optimal Python Solution (Boyer-Moore - O(1) Space)

```python
def majorityElement(nums: list[int]) -> int:
    """
    Boyer-Moore Voting Algorithm.
    If an element appears > n/2 times, it will survive cancellations.
    """
    candidate = None
    count = 0

    for num in nums:
        if count == 0:
            candidate = num

        count += (1 if num == candidate else -1)

    return candidate
```

### Complexity Analysis

- **Time Complexity**: O(n). Single pass.
- **Space Complexity**: O(1). Only two variables.

---

## 4. Majority Element II

Find all elements that appear more than `⌊n / 3⌋` times.

### Optimal Python Solution

```python
def majorityElementII(nums: list[int]) -> list[int]:
    """
    Extended Boyer-Moore for 2 candidates.
    At most 2 elements can appear > n/3 times.
    """
    cand1, cand2 = None, None
    count1, count2 = 0, 0

    for num in nums:
        if num == cand1:
            count1 += 1
        elif num == cand2:
            count2 += 1
        elif count1 == 0:
            cand1, count1 = num, 1
        elif count2 == 0:
            cand2, count2 = num, 1
        else:
            count1 -= 1
            count2 -= 1

    # Verify candidates
    res = []
    for c in [cand1, cand2]:
        if c is not None and nums.count(c) > len(nums) // 3:
            res.append(c)
    return res
```

### Complexity Analysis

- **Time Complexity**: O(n).
- **Space Complexity**: O(1).

---

## 5. First Unique Character in a String

(Same as in previous file - included for completeness of the practice list).

### Optimal Python Solution

```python
from collections import Counter

def firstUniqChar(s: str) -> int:
    counts = Counter(s)
    for i, char in enumerate(s):
        if counts[char] == 1:
            return i
    return -1
```

---

## 6. Single Number

Given a non-empty array of integers `nums`, every element appears twice except for one. Find that single one.

### Optimal Python Solution (XOR - O(1) Space)

```python
def singleNumber(nums: list[int]) -> int:
    """
    XOR property: a ^ a = 0 and a ^ 0 = a.
    XORing all numbers will cancel out pairs.
    """
    res = 0
    for num in nums:
        res ^= num
    return res
```

### Complexity Analysis

- **Time Complexity**: O(n).
- **Space Complexity**: O(1).

---

## 7. Contains Duplicate

(Discussed in Basics file). `return len(nums) != len(set(nums))` or manual set loop.

---

## 8. Contains Duplicate II

Given an integer array `nums` and an integer `k`, return `true` if there are two distinct indices `i` and `j` in the array such that `nums[i] == nums[j]` and `abs(i - j) <= k`.

### Optimal Python Solution (Sliding Window / Map)

```python
def containsNearbyDuplicate(nums: list[int], k: int) -> bool:
    seen = {} # val -> index
    for i, num in enumerate(nums):
        if num in seen and i - seen[num] <= k:
            return True
        seen[num] = i
    return False
```

---

## 9. Sort Characters By Frequency

Given a string `s`, sort it in decreasing order based on the frequency of the characters.

### Optimal Python Solution

```python
from collections import Counter

def frequencySort(s: str) -> str:
    counts = Counter(s)
    # Sort characters by frequency, then join
    sorted_chars = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    return "".join([char * freq for char, freq in sorted_chars])
```

---

## 10. Find All Duplicates in an Array

Given an integer array `nums` of length `n` where all the integers of `nums` are in the range `[1, n]` and each integer appears once or twice, return an array of all the integers that appears twice.

### Optimal Python Solution (Index Marking - O(1) Space)

```python
def findDuplicates(nums: list[int]) -> list[int]:
    """
    Use the array values as indices. Mark index as negative if visited.
    If we reach an index that is already negative, we found a duplicate.
    """
    res = []
    for num in nums:
        idx = abs(num) - 1
        if nums[idx] < 0:
            res.append(abs(num))
        else:
            nums[idx] *= -1
    return res
```
