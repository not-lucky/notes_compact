# Anagram Grouping

## Practice Problems

### 1. Valid Anagram
**Difficulty:** Easy
**Key Technique:** Counter comparison

```python
from collections import Counter

def is_anagram(s: str, t: str) -> bool:
    """
    Time: O(n)
    Space: O(1) (26 chars)
    """
    return Counter(s) == Counter(t)
```

### 2. Group Anagrams
**Difficulty:** Medium
**Key Technique:** Hashmap with sorted string as key

```python
from collections import defaultdict

def group_anagrams(strs: list[str]) -> list[list[str]]:
    """
    Time: O(n * k log k) where k is max string length
    Space: O(n * k)
    """
    groups = defaultdict(list)
    for s in strs:
        key = "".join(sorted(s))
        groups[key].append(s)
    return list(groups.values())
```

### 3. Find All Anagrams in a String
**Difficulty:** Medium
**Key Technique:** Sliding window + Counter

```python
from collections import Counter

def find_anagrams(s: str, p: str) -> list[int]:
    """
    Time: O(n)
    Space: O(1) (26 chars)
    """
    if len(p) > len(s): return []
    p_cnt = Counter(p)
    s_cnt = Counter(s[:len(p)])
    res = []
    if s_cnt == p_cnt: res.append(0)

    for i in range(len(p), len(s)):
        s_cnt[s[i]] += 1
        left_char = s[i - len(p)]
        s_cnt[left_char] -= 1
        if s_cnt[left_char] == 0:
            del s_cnt[left_char]
        if s_cnt == p_cnt:
            res.append(i - len(p) + 1)
    return res
```

### 4. Permutation in String
**Difficulty:** Medium
**Key Technique:** Sliding window + Counter

```python
from collections import Counter

def check_inclusion(s1: str, s2: str) -> bool:
    """
    Time: O(n)
    Space: O(1)
    """
    if len(s1) > len(s2): return False
    s1_cnt = Counter(s1)
    window = Counter(s2[:len(s1)])
    if window == s1_cnt: return True

    for i in range(len(s1), len(s2)):
        window[s2[i]] += 1
        left_char = s2[i - len(s1)]
        window[left_char] -= 1
        if window[left_char] == 0:
            del window[left_char]
        if window == s1_cnt:
            return True
    return False
```

### 5. Minimum Window Substring
**Difficulty:** Hard
**Key Technique:** Sliding window (expand/contract)

```python
from collections import Counter

def min_window(s: str, t: str) -> str:
    """
    Time: O(n + m)
    Space: O(m)
    """
    if not s or not t: return ""
    t_cnt = Counter(t)
    required = len(t_cnt)
    l, r = 0, 0
    formed = 0
    window_cnt = {}
    ans = float("inf"), None, None # len, l, r

    while r < len(s):
        char = s[r]
        window_cnt[char] = window_cnt.get(char, 0) + 1
        if char in t_cnt and window_cnt[char] == t_cnt[char]:
            formed += 1

        while l <= r and formed == required:
            char = s[l]
            if r - l + 1 < ans[0]:
                ans = (r - l + 1, l, r)
            window_cnt[char] -= 1
            if char in t_cnt and window_cnt[char] < t_cnt[char]:
                formed -= 1
            l += 1
        r += 1
    return "" if ans[0] == float("inf") else s[ans[1]:ans[2]+1]
```

### 6. Longest Substring Without Repeating Characters
**Difficulty:** Medium
**Key Technique:** Sliding window + Set

```python
def length_of_longest_substring(s: str) -> int:
    """
    Time: O(n)
    Space: O(min(n, 26))
    """
    chars = set()
    l = 0
    res = 0
    for r in range(len(s)):
        while s[r] in chars:
            chars.remove(s[l])
            l += 1
        chars.add(s[r])
        res = max(res, r - l + 1)
    return res
```

### 7. Longest Repeating Character Replacement
**Difficulty:** Medium
**Key Technique:** Sliding window + frequency map

```python
from collections import defaultdict

def character_replacement(s: str, k: int) -> int:
    """
    Time: O(n)
    Space: O(1)
    """
    count = defaultdict(int)
    max_f = 0
    l = 0
    res = 0
    for r in range(len(s)):
        count[s[r]] += 1
        max_f = max(max_f, count[s[r]])
        while (r - l + 1) - max_f > k:
            count[s[l]] -= 1
            l += 1
        res = max(res, r - l + 1)
    return res
```
