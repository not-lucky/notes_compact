# Practice Problems - Partition Labels

## 1. Partition Labels

### Problem Statement
You are given a string `s`. We want to partition the string into as many parts as possible so that each letter appears in at most one part.
Note that the partition is done so that after concatenating all the parts in order, the resultant string should be `s`.
Return a list of integers representing the size of these parts.

### Constraints
- `1 <= s.length <= 500`
- `s` consists of lowercase English letters.

### Example
**Input:** `s = "ababcbacadefegdehijhklij"`
**Output:** `[9,7,8]`
**Explanation:**
The partition is "ababcbaca", "defegde", "hijhklij".
This is a partition so that each letter appears in at most one part.
A partition like "ababcbacadefegde", "hijhklij" is incorrect, because it splits s into less parts.

### Python Implementation
```python
def partitionLabels(s: str) -> list[int]:
    last = {c: i for i, c in enumerate(s)}
    res = []
    start = 0
    end = 0
    for i, c in enumerate(s):
        end = max(end, last[c])
        if i == end:
            res.append(i - start + 1)
            start = i + 1
    return res
```

## 2. Maximum Number of Non-overlapping Substrings

### Problem Statement
Given a string `s` of lowercase letters, you need to find the maximum number of non-empty substrings of `s` that meet these conditions:
1. The substrings do not overlap, that is for any two substrings `s[i..j]` and `s[k..l]`, either `j < k` or `l < i` is true.
2. A substring that contains a certain character `c` must also contain all occurrences of `c`.
Find the maximum number of substrings that meet the above conditions. If there are multiple answers with the same number of substrings, return the one with minimum total length. It can be shown that the answer is unique.

### Constraints
- `1 <= s.length <= 10^5`
- `s` contains only lowercase English letters.

### Example
**Input:** `s = "adefaddaccc"`
**Output:** `["e","f","ccc"]`

### Python Implementation
```python
def maxNumOfSubstrings(s: str) -> list[str]:
    # Find first and last occurrence of each character
    first = {c: i for i, c in enumerate(s[::-1])}
    first = {c: len(s) - 1 - i for c, i in first.items()}
    last = {c: i for i, c in enumerate(s)}
    for c in first:
        # Re-calculating first since the logic above was slightly confusing
        pass

    first = {}
    for i, c in enumerate(s):
        if c not in first: first[c] = i

    def get_end(i):
        end = last[s[i]]
        j = i
        while j <= end:
            if first[s[j]] < i: return -1
            end = max(end, last[s[j]])
            j += 1
        return end

    res = []
    prev_end = -1
    # Store all valid intervals
    intervals = []
    for i in range(len(s)):
        if i == first[s[i]]:
            end = get_end(i)
            if end != -1:
                intervals.append((i, end))

    # Greedy: select intervals that end earliest
    intervals.sort(key=lambda x: x[1])
    for start, end in intervals:
        if start > prev_end:
            res.append(s[start:end+1])
            prev_end = end
    return res
```

## 3. Optimal Partition of String

### Problem Statement
Given a string `s`, partition the string into one or more substrings such that the characters in each substring are unique. That is, no letter appears in a single substring more than once.
Return the minimum number of substrings in such a partition.
Note that each character should belong to exactly one substring in a partition.

### Constraints
- `1 <= s.length <= 10^5`
- `s` consists of lowercase English letters.

### Example
**Input:** `s = "abacaba"`
**Output:** `4`
**Explanation:** Two such partitions are ("a","ba","ca","ba") and ("ab","ac","ab","a").
It can be shown that 4 is the minimum number of substrings needed.

### Python Implementation
```python
def partitionString(s: str) -> int:
    res = 1
    seen = set()
    for c in s:
        if c in seen:
            res += 1
            seen = {c}
        else:
            seen.add(c)
    return res
```
