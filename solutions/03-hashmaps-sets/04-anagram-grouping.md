# Solution: Anagram Grouping

## Problem Statement
Given an array of strings `strs`, group the anagrams together. You can return the answer in any order.

## Constraints
- `1 <= strs.length <= 10^4`
- `0 <= strs[i].length <= 100`
- `strs[i]` consists of lowercase English letters.

## Example (Input/Output)
```python
Input: strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
Output: [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]
```

## Python Implementation
```python
from collections import defaultdict

def group_anagrams(strs: list[str]) -> list[list[str]]:
    """
    Group strings that are anagrams of each other.

    Time: O(n * k log k) where k = max string length
    Space: O(n * k)
    """
    groups = defaultdict(list)

    for s in strs:
        # Signature: sorted string
        key = "".join(sorted(s))
        groups[key].append(s)

    return list(groups.values())
```
