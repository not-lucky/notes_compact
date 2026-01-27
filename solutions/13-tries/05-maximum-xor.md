# Solutions: Bitwise Trie & Maximum XOR

## 1. Maximum XOR of Two Numbers in an Array
(LeetCode 421)

### Problem Statement
Given an integer array `nums`, return the maximum result of `nums[i] XOR nums[j]`, where `0 <= i <= j < n`.

### Examples & Edge Cases
**Example:**
```
Input: nums = [3,10,5,25,2,8]
Output: 28 (5 XOR 25)
```

### Optimal Python Solution
```python
class Solution:
    def findMaximumXOR(self, nums: list[int]) -> int:
        # Determine bit length of the largest number
        L = max(nums).bit_length()
        root = {}
        max_xor = 0

        for num in nums:
            node = root
            search_node = root
            curr_xor = 0

            # Single pass: attempt to find max XOR with existing numbers,
            # then insert current number into the Trie.
            for i in range(L - 1, -1, -1):
                bit = (num >> i) & 1
                toggled_bit = 1 - bit

                # Search: Can we find the opposite bit to maximize XOR?
                if toggled_bit in search_node:
                    curr_xor |= (1 << i)
                    search_node = search_node[toggled_bit]
                elif bit in search_node:
                    search_node = search_node[bit]

                # Insert: Build the trie path for the current number
                if bit not in node:
                    node[bit] = {}
                node = node[bit]

            max_xor = max(max_xor, curr_xor)

        return max_xor
```

### Explanation
1.  **Greedy Strategy**: To maximize XOR, we want the most significant bits (MSB) to be 1. This happens when the bits of the two numbers are different.
2.  **Bitwise Trie**: We store numbers as binary paths (e.g., `0101` is a path of `0->1->0->1`).
3.  **Toggled Bit Search**: For each number, we traverse the Trie and always try to take the path of the `toggled_bit` (if `0` we want `1`, if `1` we want `0`). If it exists, the XOR result at that bit position becomes `1`.

### Complexity Analysis
*   **Time Complexity**: $O(N \times L)$ where $N$ is the number of elements and $L$ is the number of bits (e.g., 31 for 32-bit integers). We perform one insertion and one search per number, and each operation involves traversing $L$ levels in the Trie.
*   **Space Complexity**: $O(N \times L)$ to store all numbers in the bitwise Trie, where each node represents a single bit.

---

## 2. Maximum XOR With an Element From Array
(LeetCode 1707)

### Problem Statement
You are given an array `nums` and a 2D array `queries` where `queries[i] = [xi, mi]`. The answer to the $i$-th query is the maximum bitwise XOR value of `xi` and any element of `nums` that does not exceed `mi`. If all elements in `nums` exceed `mi`, the answer is -1.

### Optimal Python Solution
```python
class Solution:
    def maximizeXor(self, nums: list[int], queries: list[list[int]]) -> list[int]:
        nums.sort()
        # Sort queries by 'm' to process them "offline"
        sorted_queries = sorted(enumerate(queries), key=lambda x: x[1][1])

        trie = {}
        res = [-1] * len(queries)
        nums_idx = 0

        for q_idx, (x, m) in sorted_queries:
            # Add all numbers <= m to the Trie
            while nums_idx < len(nums) and nums[nums_idx] <= m:
                num = nums[nums_idx]
                node = trie
                for i in range(31, -1, -1):
                    bit = (num >> i) & 1
                    node = node.setdefault(bit, {})
                nums_idx += 1

            # Query the Trie for max XOR with 'x'
            if not trie:
                continue

            node = trie
            curr_xor = 0
            for i in range(31, -1, -1):
                bit = (x >> i) & 1
                toggled = 1 - bit
                if toggled in node:
                    curr_xor |= (1 << i)
                    node = node[toggled]
                else:
                    node = node[bit]
            res[q_idx] = curr_xor

        return res
```

### Explanation
1.  **Offline Queries**: By sorting both `nums` and `queries` (by the threshold `m`), we can incrementally build the Trie. We only add numbers to the Trie when they become "eligible" for the current query's threshold.
2.  **Bitwise Search**: Once eligible numbers are in the Trie, we use the standard Maximum XOR search logic.

### Complexity Analysis
*   **Time Complexity**: $O(N \log N + Q \log Q + (N + Q) \times 31)$ where $N$ is the number of elements and $Q$ is the number of queries. We sort both inputs ($O(N \log N + Q \log Q)$) and then process each element and query exactly once, traversing 31 bits each time.
*   **Space Complexity**: $O(N \times 31 + Q)$ to store the Trie and the result array.

---

## 3. Maximum Genetic Difference Query
(LeetCode 1938)

### Problem Statement
Given a tree and queries `[node, val]`, find the maximum XOR of `val` with any node on the path from the root to `node`.

### Optimal Python Solution
```python
from collections import defaultdict

class Solution:
    def maxGeneticDifference(self, parents: list[int], queries: list[list[int]]) -> list[int]:
        # Build adjacency list
        tree = defaultdict(list)
        root = -1
        for i, p in enumerate(parents):
            if p == -1: root = i
            else: tree[p].append(i)

        # Map queries to their respective nodes
        node_to_queries = defaultdict(list)
        for i, (node, val) in enumerate(queries):
            node_to_queries[node].append((val, i))

        trie = {}
        ans = [0] * len(queries)

        def update(num, delta):
            node = trie
            for i in range(19, -1, -1):
                bit = (num >> i) & 1
                node = node.setdefault(bit, {'cnt': 0})
                node['cnt'] += delta
                node = node

        def query(val):
            node = trie
            res = 0
            for i in range(19, -1, -1):
                bit = (val >> i) & 1
                toggled = 1 - bit
                if toggled in node and node[toggled]['cnt'] > 0:
                    res |= (1 << i)
                    node = node[toggled]
                else:
                    node = node[bit]
            return res

        def dfs(u):
            # Add current node to trie
            node = trie
            for i in range(19, -1, -1):
                bit = (u >> i) & 1
                node = node.setdefault(bit, {'cnt': 0})
                node['cnt'] += 1
                node = node[bit]

            for val, q_idx in node_to_queries[u]:
                ans[q_idx] = query(val)

            for v in tree[u]:
                dfs(v)

            # Backtrack: Remove current node from trie
            node = trie
            for i in range(19, -1, -1):
                bit = (u >> i) & 1
                node = node[bit]
                node['cnt'] -= 1

        dfs(root)
        return ans
```

### Explanation
1.  **DFS + Backtracking**: As we traverse from root to leaf, we add nodes to a global Trie. After exploring a node's entire subtree, we remove it from the Trie (backtrack).
2.  **Path Invariant**: At any point in the DFS, the Trie contains exactly the nodes on the path from the root to the current node.
3.  **Count-based Trie**: Since we are adding/removing nodes, each Trie node must store a `cnt` to know if a branch is still "active".

### Complexity Analysis
*   **Time Complexity**: $O((N + Q) \times 20)$ where $N$ is the number of tree nodes and $Q$ is the number of queries. We traverse each node of the tree once via DFS and process all queries for that node, with each Trie operation (insert, query, remove) taking $O(20)$ bitwise steps.
*   **Space Complexity**: $O(N \times 20 + Q)$ for the Trie storage and the query mapping.

---

## 4. Count Pairs With XOR in a Range
(LeetCode 1803)

### Problem Statement
Given an array `nums` and two integers `low` and `high`, return the number of pairs `(i, j)` such that `0 <= i < j < n` and `low <= (nums[i] XOR nums[j]) <= high`.

### Optimal Python Solution
```python
class Solution:
    def countPairs(self, nums: list[int], low: int, high: int) -> int:
        def count_less_than(limit):
            root = {}
            count = 0
            for x in nums:
                node = root
                for i in range(15, -1, -1):
                    if not node: break
                    bit_x = (x >> i) & 1
                    bit_limit = (limit >> i) & 1

                    if bit_limit == 1:
                        # If limit bit is 1, XORing with bit_x gives 0, which is < 1.
                        # All numbers in the bit_x branch are valid.
                        if bit_x in node:
                            count += node[bit_x]['cnt']
                        # Continue searching in the toggled branch (XOR = 1)
                        node = node.get(1 - bit_x)
                    else:
                        # If limit bit is 0, we MUST have XOR = 0 to stay < limit.
                        # So we must follow the bit_x branch.
                        node = node.get(bit_x)

                # Insert x into Trie
                node = root
                for i in range(15, -1, -1):
                    bit = (x >> i) & 1
                    node = node.setdefault(bit, {'cnt': 0})
                    node['cnt'] += 1
                    node = node[bit]
            return count

        # Pairs in range [low, high] = (pairs < high + 1) - (pairs < low)
        return count_less_than(high + 1) - count_less_than(low)
```

### Explanation
1.  **Range to Prefix Sum**: `count(low <= XOR <= high)` is equivalent to `count(XOR < high + 1) - count(XOR < low)`.
2.  **Bitwise Digit-by-Digit**: When comparing `XOR` with a `limit`, if the $i$-th bit of the `limit` is 1, then any number that produces an `XOR` bit of 0 at that position is strictly less than the `limit`. We add all counts from that subtree and continue searching.

### Complexity Analysis
*   **Time Complexity**: $O(N \times 16)$ where $N$ is the number of elements. We process each number twice (once for `high` and once for `low`), performing $O(16)$ bitwise operations per number in each pass.
*   **Space Complexity**: $O(N \times 16)$ to store the bitwise Trie for each counting pass.

---

## 5. Maximum XOR After Operations
(LeetCode 2317)

### Problem Statement
You are given an array `nums`. In one operation, you can select any `nums[i]` and replace it with `nums[i] AND (nums[i] XOR x)` for any integer `x`. Return the maximum possible bitwise XOR of all elements of `nums` after any number of operations.

### Optimal Python Solution
```python
class Solution:
    def maximumXOR(self, nums: list[int]) -> int:
        # The operation "nums[i] AND (nums[i] XOR x)" essentially allows us
        # to flip any 1-bit in nums[i] to a 0-bit.
        # It does NOT allow us to flip a 0-bit to a 1-bit.
        # To maximize the total XOR, we want the result to have a 1 at
        # every bit position where at least one number in the original
        # array has a 1.
        res = 0
        for n in nums:
            res |= n
        return res
```

### Explanation
1.  **Observation**: The operation `n & (n ^ x)` is equivalent to `n & some_value`. This means we can unset any bit of `n`, but we can never set a bit that was originally 0.
2.  **Optimization**: To maximize `n1 ^ n2 ^ ... ^ nk`, we want as many 1s as possible. If any `nums[i]` has a 1 at bit `j`, we can choose to keep exactly one such 1 across all numbers and zero out all other 1s at bit `j`. This results in bit `j` being 1 in the final XOR.
3.  **Result**: The answer is simply the bitwise OR of all numbers.

### Complexity Analysis
*   **Time Complexity**: $O(N)$ where $N$ is the number of elements in the array. We perform a single bitwise OR operation across all numbers.
*   **Space Complexity**: $O(1)$ extra space, as we only maintain a single result variable.
