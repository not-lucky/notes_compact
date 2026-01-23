# Solution: Maximum XOR Practice Problems

## Problem 1: Maximum XOR of Two Numbers in an Array
### Problem Statement
Given an integer array `nums`, return the maximum result of `nums[i] XOR nums[j]`, where `0 <= i <= j < n`.

### Python Implementation
```python
class Solution:
    def findMaximumXOR(self, nums: list[int]) -> int:
        L = max(nums).bit_length()
        root = {}
        max_xor = 0

        for num in nums:
            node = root
            for i in range(L - 1, -1, -1):
                bit = (num >> i) & 1
                if bit not in node:
                    node[bit] = {}
                node = node[bit]

            node = root
            curr_xor = 0
            for i in range(L - 1, -1, -1):
                bit = (num >> i) & 1
                want = 1 - bit
                if want in node:
                    curr_xor |= (1 << i)
                    node = node[want]
                else:
                    node = node[bit]
            max_xor = max(max_xor, curr_xor)

        return max_xor
```

---

## Problem 2: Maximum XOR With an Element From Array
### Problem Statement
You are given an array `nums` consisting of non-negative integers. You are also given a `queries` array, where `queries[i] = [xi, mi]`.

The answer to the `i`th query is the maximum bitwise XOR value of `xi` and any element of `nums` that does not exceed `mi`. If all elements in `nums` are greater than `mi`, then the answer is `-1`.

Return an answer array `answer` where `answer[i]` is the answer to the `i`th query.

### Python Implementation
```python
class Solution:
    def maximizeXor(self, nums: list[int], queries: list[list[int]]) -> list[int]:
        nums.sort()
        q = sorted([(m, x, i) for i, (x, m) in enumerate(queries)])
        res = [-1] * len(queries)
        trie = {}
        idx = 0

        def insert(val):
            node = trie
            for i in range(30, -1, -1):
                bit = (val >> i) & 1
                if bit not in node:
                    node[bit] = {}
                node = node[bit]

        def query(val):
            node = trie
            ans = 0
            for i in range(30, -1, -1):
                bit = (val >> i) & 1
                want = 1 - bit
                if want in node:
                    ans |= (1 << i)
                    node = node[want]
                else:
                    node = node[bit]
            return ans

        for m, x, i in q:
            while idx < len(nums) and nums[idx] <= m:
                insert(nums[idx])
                idx += 1
            if trie:
                res[i] = query(x)
        return res
```
