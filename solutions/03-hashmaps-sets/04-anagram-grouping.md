# Anagram Grouping - Solutions

## 1. Valid Anagram
Given two strings `s` and `t`, return `true` if `t` is an anagram of `s`, and `false` otherwise.

### Problem Statement
Check if two strings contain the exact same characters with the same frequencies.

### Examples & Edge Cases
**Example 1:**
- Input: `s = "anagram"`, `t = "nagaram"`
- Output: `true`

**Example 2:**
- Input: `s = "rat"`, `t = "car"`
- Output: `false`

### Optimal Python Solution
```python
from collections import Counter

def isAnagram(s: str, t: str) -> bool:
    """
    Two strings are anagrams if their character counts are identical.
    """
    if len(s) != len(t):
        return False

    return Counter(s) == Counter(t)
```

### Explanation
An anagram means the strings have the same "inventory" of characters. By comparing the frequency counts of both strings, we can determine if they are anagrams. If lengths differ, they cannot be anagrams.

### Complexity Analysis
- **Time Complexity**: O(n), where n is the length of the strings.
- **Space Complexity**: O(k), where k is the size of the alphabet (e.g., 26 for lowercase English).

---

## 2. Group Anagrams
Given an array of strings `strs`, group the anagrams together. You can return the answer in any order.

### Problem Statement
Group strings that share the same characters.

### Examples & Edge Cases
**Example:**
- Input: `strs = ["eat", "tea", "tan", "ate", "nat", "bat"]`
- Output: `[["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]`

### Optimal Python Solution
```python
from collections import defaultdict

def groupAnagrams(strs: list[str]) -> list[list[str]]:
    """
    Use a sorted version of each string as a canonical key in a hashmap.
    """
    groups = defaultdict(list)

    for s in strs:
        # Sort characters to get the 'canonical' form of the anagram
        key = tuple(sorted(s)) # Tuples are hashable and can be dict keys
        groups[key].append(s)

    return list(groups.values())
```

### Explanation
All anagrams, when their characters are sorted alphabetically, result in the same string. We use this sorted string (as a tuple) as a key in a dictionary to collect all strings that belong to that anagram group.

### Complexity Analysis
- **Time Complexity**: O(n * k log k), where n is the number of strings and k is the maximum length of a string (due to sorting each string).
- **Space Complexity**: O(n * k) to store all strings in the hashmap.

---

## 3. Find All Anagrams in a String
Given two strings `s` and `p`, return an array of all the start indices of `p`'s anagrams in `s`.

### Optimal Python Solution (Sliding Window)
```python
from collections import Counter

def findAnagrams(s: str, p: str) -> list[int]:
    """
    Use a sliding window of length len(p).
    Maintain a frequency count of the current window and compare with p.
    """
    n, m = len(s), len(p)
    if m > n: return []

    p_counts = Counter(p)
    window_counts = Counter(s[:m])
    res = []

    if window_counts == p_counts:
        res.append(0)

    for i in range(m, n):
        # Add new char, remove old char from window
        window_counts[s[i]] += 1
        window_counts[s[i-m]] -= 1

        # Clean up zero counts for comparison
        if window_counts[s[i-m]] == 0:
            del window_counts[s[i-m]]

        if window_counts == p_counts:
            res.append(i - m + 1)

    return res
```

### Complexity Analysis
- **Time Complexity**: O(n). We visit each character once. Comparing fixed-size counters (alphabet size) is O(1).
- **Space Complexity**: O(1) (space for alphabet frequency map).

---

## 4. Permutation in String
Given two strings `s1` and `s2`, return `true` if `s2` contains a permutation of `s1`.

### Optimal Python Solution
Identical logic to "Find All Anagrams". Check if any window in `s2` is an anagram of `s1`.

---

## 5. Minimum Window Substring
Given two strings `s` and `t`, return the minimum window substring of `s` such that every character in `t` (including duplicates) is included in the window.

### Optimal Python Solution
```python
from collections import Counter

def minWindow(s: str, t: str) -> str:
    if not t or not s: return ""

    dict_t = Counter(t)
    required = len(dict_t)
    l, r = 0, 0
    formed = 0
    window_counts = {}

    # (length, left, right)
    ans = float("inf"), None, None

    while r < len(s):
        char = s[r]
        window_counts[char] = window_counts.get(char, 0) + 1

        if char in dict_t and window_counts[char] == dict_t[char]:
            formed += 1

        # Try to contract the window
        while l <= r and formed == required:
            char = s[l]
            if r - l + 1 < ans[0]:
                ans = (r - l + 1, l, r)

            window_counts[char] -= 1
            if char in dict_t and window_counts[char] < dict_t[char]:
                formed -= 1
            l += 1
        r += 1

    return "" if ans[0] == float("inf") else s[ans[1] : ans[2] + 1]
```

### Complexity Analysis
- **Time Complexity**: O(n + m).
- **Space Complexity**: O(n + m).

---

## 6. Longest Substring Without Repeating Characters
Given a string `s`, find the length of the longest substring without repeating characters.

### Optimal Python Solution
```python
def lengthOfLongestSubstring(s: str) -> int:
    char_map = {} # char -> index
    max_len = 0
    start = 0

    for end, char in enumerate(s):
        if char in char_map and char_map[char] >= start:
            start = char_map[char] + 1

        char_map[char] = end
        max_len = max(max_len, end - start + 1)

    return max_len
```

---

## 7. Longest Repeating Character Replacement
You are given a string `s` and an integer `k`. You can choose any character of the string and change it to any other uppercase English character. You can perform this operation at most `k` times. Return the length of the longest substring containing the same letter you can get after performing the above operations.

### Optimal Python Solution
```python
from collections import defaultdict

def characterReplacement(s: str, k: int) -> int:
    count = defaultdict(int)
    max_f = 0
    l = 0
    res = 0

    for r in range(len(s)):
        count[s[r]] += 1
        max_f = max(max_f, count[s[r]])

        # Window is valid if (length - max_freq) <= k
        while (r - l + 1) - max_f > k:
            count[s[l]] -= 1
            l += 1
        res = max(res, r - l + 1)
    return res
```

---

## 8. Smallest Window Containing Substring
(Usually refers to same logic as Minimum Window Substring or finding shortest substring containing all unique characters of a string).
Implemented similarly with sliding window and frequency map.
O(n) Time, O(k) Space.
