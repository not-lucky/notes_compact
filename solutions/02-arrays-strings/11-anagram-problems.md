# Anagram Problems - Solutions

## Practice Problems

### 1. Valid Anagram
**Problem Statement**: Given two strings `s` and `t`, return `true` if `t` is an anagram of `s`, and `false` otherwise.

**Examples & Edge Cases**:
- Example: `s = "anagram", t = "nagaram"` -> `true`
- Edge Case: Strings of different lengths.
- Edge Case: Case sensitivity (usually assume lowercase in interviews).

**Optimal Python Solution**:
```python
from collections import Counter

def isAnagram(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False

    # Using a frequency array for O(1) space (limited alphabet)
    count = [0] * 26
    for char in s:
        count[ord(char) - ord('a')] += 1
    for char in t:
        count[ord(char) - ord('a')] -= 1
        # If any count goes below zero, it's not an anagram
        if count[ord(char) - ord('a')] < 0:
            return False

    return True
```

**Explanation**:
An anagram must have the same characters with the same frequencies. We use an array of size 26 to store counts of 'a'-'z'. We increment for `s` and decrement for `t`. If all counts return to zero (and lengths were equal), they are anagrams.

**Complexity Analysis**:
- **Time Complexity**: O(n), where n is the length of the strings.
- **Space Complexity**: O(1), since the array size is constant (26).

---

### 2. Group Anagrams
**Problem Statement**: Given an array of strings `strs`, group the anagrams together. You can return the answer in any order.

**Optimal Python Solution**:
```python
from collections import defaultdict

def groupAnagrams(strs: list[str]) -> list[list[str]]:
    # Map a canonical representation of an anagram to its group of strings
    groups = defaultdict(list)

    for s in strs:
        # Canonical form 1: Sorted string
        # key = "".join(sorted(s))

        # Canonical form 2: Character count tuple (More efficient for long strings)
        count = [0] * 26
        for char in s:
            count[ord(char) - ord('a')] += 1
        key = tuple(count)

        groups[key].append(s)

    return list(groups.values())
```

**Explanation**:
We need a way to map different anagrams to the same bucket. Two strings are anagrams if their sorted versions are identical or if their character frequency counts are identical. Using the frequency count tuple as a dictionary key allows us to group them in linear time relative to the total number of characters.

**Complexity Analysis**:
- **Time Complexity**: O(N * K), where N is the number of strings and K is the maximum length of a string.
- **Space Complexity**: O(N * K).

---

### 3. Find All Anagrams in a String
**Problem Statement**: Find all start indices of `p`'s anagrams in `s`.

**Optimal Python Solution**:
```python
def findAnagrams(s: str, p: str) -> list[int]:
    ns, np = len(s), len(p)
    if ns < np: return []

    p_count = [0] * 26
    s_count = [0] * 26
    for char in p:
        p_count[ord(char) - ord('a')] += 1

    res = []
    for i in range(ns):
        # Add current character
        s_count[ord(s[i]) - ord('a')] += 1

        # Remove character that left the window
        if i >= np:
            s_count[ord(s[i - np]) - ord('a')] -= 1

        # Compare frequency arrays
        if s_count == p_count:
            res.append(i - np + 1)

    return res
```

**Explanation**:
We use a fixed-size sliding window of length `len(p)`. We maintain the character counts of the current window and compare it to the character counts of `p`.

**Complexity Analysis**:
- **Time Complexity**: O(N), where N is length of `s`. Array comparison `s_count == p_count` takes O(26) = O(1).
- **Space Complexity**: O(1).

---

### 4. Permutation in String
**Problem Statement**: Given two strings `s1` and `s2`, return `true` if `s2` contains a permutation of `s1`.

**Optimal Python Solution**:
```python
def checkInclusion(s1: str, s2: str) -> bool:
    n1, n2 = len(s1), len(s2)
    if n1 > n2: return False

    cnt1 = [0] * 26
    cnt2 = [0] * 26
    for i in range(n1):
        cnt1[ord(s1[i]) - ord('a')] += 1
        cnt2[ord(s2[i]) - ord('a')] += 1

    if cnt1 == cnt2: return True

    for i in range(n1, n2):
        cnt2[ord(s2[i]) - ord('a')] += 1
        cnt2[ord(s2[i-n1]) - ord('a')] -= 1
        if cnt1 == cnt2:
            return True

    return False
```

**Explanation**:
This is identical to "Find All Anagrams", but we return `True` as soon as one match is found.

**Complexity Analysis**:
- **Time Complexity**: O(N).
- **Space Complexity**: O(1).

---

### 5. Minimum Number of Steps to Make Two Strings Anagrams
**Problem Statement**: You are given two strings of the same length `s` and `t`. In one step, you can choose any character of `t` and replace it with another character. Return the minimum number of steps to make `t` an anagram of `s`.

**Optimal Python Solution**:
```python
from collections import Counter

def minSteps(s: str, t: str) -> int:
    s_count = Counter(s)
    t_count = Counter(t)

    steps = 0
    for char, count in s_count.items():
        if count > t_count[char]:
            # We need 'count' occurrences of 'char', but t only has 't_count[char]'
            # The difference must be replaced by changing some other chars in t
            steps += count - t_count[char]

    return steps
```

**Explanation**:
Since the strings have the same length, we just need to see how many characters in `s` are missing or under-represented in `t`. For every character in `s` that appears more times than it does in `t`, we must perform that many replacements in `t`.

**Complexity Analysis**:
- **Time Complexity**: O(N).
- **Space Complexity**: O(1) (alphabet size).

---

### 6. Smallest Range Covering Elements from K Lists
**Problem Statement**: You have `k` lists of sorted integers in non-decreasing order. Find the smallest range that includes at least one number from each of the `k` lists.

**Optimal Python Solution**:
```python
import heapq

def smallestRange(nums: list[list[int]]) -> list[int]:
    # Min-heap stores (value, list_index, element_index)
    pq = []
    max_val = float('-inf')

    # Initial state: first element from each list
    for i in range(len(nums)):
        heapq.heappush(pq, (nums[i][0], i, 0))
        max_val = max(max_val, nums[i][0])

    res = [float('-inf'), float('inf')]

    while len(pq) == len(nums):
        min_val, r, c = heapq.heappop(pq)

        # Update result if current range [min_val, max_val] is smaller
        if max_val - min_val < res[1] - res[0]:
            res = [min_val, max_val]

        # Move to the next element in the list that provided the min_val
        if c + 1 < len(nums[r]):
            next_val = nums[r][c + 1]
            heapq.heappush(pq, (next_val, r, c + 1))
            max_val = max(max_val, next_val)

    return res
```

**Explanation**:
We want to keep one element from each list and minimize the difference between the max and min of those elements. We use a min-heap to always track the smallest element currently in our set of `k` elements. When we remove the minimum, we must replace it with the next element from the same list to maintain the "one from each list" property.

**Complexity Analysis**:
- **Time Complexity**: O(N log k), where N is the total number of elements.
- **Space Complexity**: O(k).

---

### 7. Scramble String
**Problem Statement**: Determine if `s2` is a scrambled version of `s1`.

**Optimal Python Solution**:
```python
from functools import lru_cache

class Solution:
    @lru_cache(None)
    def isScramble(self, s1: str, s2: str) -> bool:
        if s1 == s2:
            return True
        if sorted(s1) != sorted(s2): # Anagram check as a pruning step
            return False

        n = len(s1)
        for i in range(1, n):
            # No swap case
            if self.isScramble(s1[:i], s2[:i]) and self.isScramble(s1[i:], s2[i:]):
                return True
            # Swap case
            if self.isScramble(s1[:i], s2[n-i:]) and self.isScramble(s1[i:], s2[:n-i]):
                return True

        return False
```

**Explanation**:
This is a recursive problem with memoization. A string `s1` can be scrambled into `s2` if there exists a split point such that the two parts of `s1` match the two parts of `s2` (either directly or swapped). The anagram check `sorted(s1) != sorted(s2)` is a crucial pruning step.

**Complexity Analysis**:
- **Time Complexity**: O(N^4) roughly, due to memoization and the loop.
- **Space Complexity**: O(N^3).
