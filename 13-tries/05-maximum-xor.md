# Maximum XOR of Two Numbers (Bitwise Trie)

> **Prerequisites:** [Trie Implementation](./01-trie-implementation.md), [Bit Manipulation](../15-bit-manipulation/README.md)

## Interview Context

"Maximum XOR of Two Numbers in an Array" (LeetCode 421) introduces the powerful technique of using tries for bit manipulation problems. This is a favorite at Google and Microsoft because it combines two non-obvious concepts: tries and XOR properties.

---

## Building Intuition

**Why XOR is Special**

XOR has a beautiful property: the result is 1 when bits differ:

```
0 XOR 0 = 0  (same → 0)
0 XOR 1 = 1  (different → 1)
1 XOR 0 = 1  (different → 1)
1 XOR 1 = 0  (same → 0)
```

To MAXIMIZE XOR, you want as many 1s as possible in the result. That means you want OPPOSITE bits at each position.

**The Greedy Insight: MSB First**

Higher bits matter exponentially more:

```
Bit 7 = 128    (2^7)
Bit 6 = 64     (2^6)
...
Bit 0 = 1      (2^0)

Getting bit 7 right is worth more than ALL lower bits combined:
  10000000 = 128 > 01111111 = 127

Therefore: Maximize from the most significant bit (MSB) down.
```

**Why a Trie?**

The naive approach compares all pairs: O(n²). But we can do better by thinking about it differently:

For each number X, we want to find Y such that X XOR Y is maximized. If we know all bits of X, we can greedily pick Y bit-by-bit:

```
X = 10110 (binary)

To maximize X XOR Y:
  Bit 4 of X is 1 → Want bit 4 of Y to be 0
  Bit 3 of X is 0 → Want bit 3 of Y to be 1
  Bit 2 of X is 1 → Want bit 2 of Y to be 0
  ... and so on

The trie lets us check "Does any number have bit 0 at position 4?"
in O(1) per bit check.
```

**Visualizing the Bitwise Trie**

Numbers become binary paths:

```
Numbers: 3 (011), 5 (101), 7 (111)

Trie (MSB first, 3 bits):
        root
       /    \
      0      1
      |     / \
      1    0   1
      |    |   |
      1    1   1
     (3)  (5) (7)

Each root-to-leaf path is a number's binary representation.
```

**The Query Process**

For X = 5 (101), find Y that maximizes XOR:

```
Bit 2: X has 1, want 0. Is there a 0 child? YES → take it, XOR gets 1
Bit 1: X has 0, want 1. Is there a 1 child? YES → take it, XOR gets 1
Bit 0: X has 1, want 0. Is there a 0 child? NO → take 1, XOR gets 0

Path taken: 011 = 3
XOR = 101 XOR 011 = 110 = 6
```

**Why This is O(n × L) Instead of O(n²)**

```
Brute force: Compare all pairs
  n numbers → n(n-1)/2 pairs → O(n²)

Trie approach:
  Build trie: n numbers × L bits = O(n × L)
  Query each: n numbers × L bits = O(n × L)
  Total: O(n × L) where L = 32 for integers

For n = 100,000 and L = 32:
  Brute force: 5 × 10⁹ comparisons
  Trie: 3.2 × 10⁶ operations

~1500x faster!
```

---

## When NOT to Use This Pattern

**1. Finding XOR of Consecutive Range**

For "XOR of numbers from L to R", use the mathematical property:

```python
def xor_range(L, R):
    # XOR from 1 to n has a pattern based on n % 4
    def xor_1_to_n(n):
        if n % 4 == 0: return n
        if n % 4 == 1: return 1
        if n % 4 == 2: return n + 1
        return 0

    return xor_1_to_n(R) ^ xor_1_to_n(L - 1)
```

No trie needed—this is O(1).

**2. XOR Sum of All Pairs**

If you need the total XOR of all pairs (not maximum), use bit counting:

```python
# For each bit position, count how many numbers have 1 there
# Pairs with different bits contribute to that bit's sum
# This is O(n × L), but simpler than trie
```

**3. Small n Where O(n²) is Acceptable**

For n = 100, brute force is 5,000 comparisons. Trie setup might have higher constant factor.

**4. Negative Numbers**

XOR on signed integers is tricky. The sign bit can mess up the MSB-first greedy approach. You'd need to handle two's complement carefully.

**Red Flags:**
- "XOR of range" → Use mathematical formula
- "Count pairs with XOR = K" → Hashmap counting better
- "XOR exists/doesn't exist" → Hashmap sufficient
- Negative numbers without clarification → Ask interviewer

---

## Problem Statement

Given an integer array `nums`, return the maximum result of `nums[i] XOR nums[j]`, where `0 <= i <= j < n`.

```
Input: nums = [3, 10, 5, 25, 2, 8]
Output: 28
Explanation: 5 XOR 25 = 28 (maximum XOR pair)

Binary:
5  = 00101
25 = 11001
XOR= 11100 = 28
```

---

## Pattern: Bitwise Trie

### Key Insight

To maximize XOR, for each bit position, we want opposite bits (1 XOR 0 = 1).

**Strategy**: Build a trie where:
- Each node has at most 2 children: 0 and 1
- Each path from root to leaf represents a number's binary form
- For each number, traverse the trie trying to take the opposite bit at each level

### Visualization

```
Numbers: [3, 10, 5, 25]
Binary (5 bits):
3  = 00011
10 = 01010
5  = 00101
25 = 11001

Trie (built bit by bit, MSB first):
              root
             /    \
            0      1
           /        \
          0          1
         / \          \
        0   1          0
       /   /            \
      1   0              0
     /   /                \
    1   1                  1
   (3) (10)              (25)
         |
         0
         |
         1
        (5)

For num=5 (00101), find max XOR:
  Bit 4: have 0, want 1 → take 1 (exists: 25's path)
  Bit 3: have 0, want 1 → take 1 (exists)
  Bit 2: have 1, want 0 → take 0 (exists)
  Bit 1: have 0, want 1 → no 1, take 0
  Bit 0: have 1, want 0 → take 0 (exists)
  Path: 11000 → XOR with 00101 = 11101 = 29? Wait, let's recalculate...

Actually 5 XOR 25 = 28:
  5  = 00101
  25 = 11001
  XOR= 11100 = 28 ✓
```

---

## Implementation

### Standard Solution

```python
class Solution:
    def findMaximumXOR(self, nums: list[int]) -> int:
        """
        Find maximum XOR of any two numbers in array.

        Time: O(n × 32) = O(n) for 32-bit integers
        Space: O(n × 32) = O(n) for trie
        """
        # Determine number of bits needed
        max_num = max(nums)
        if max_num == 0:
            return 0
        L = max_num.bit_length()

        # Build trie
        root = {}
        for num in nums:
            node = root
            for i in range(L - 1, -1, -1):  # MSB to LSB
                bit = (num >> i) & 1
                if bit not in node:
                    node[bit] = {}
                node = node[bit]

        # Find max XOR for each number
        max_xor = 0
        for num in nums:
            node = root
            curr_xor = 0
            for i in range(L - 1, -1, -1):
                bit = (num >> i) & 1
                want = 1 - bit  # Opposite bit

                if want in node:
                    curr_xor |= (1 << i)  # This bit contributes to XOR
                    node = node[want]
                else:
                    node = node[bit]

            max_xor = max(max_xor, curr_xor)

        return max_xor
```

### With Explicit TrieNode Class

```python
class TrieNode:
    def __init__(self):
        self.children = {}  # 0 or 1 -> TrieNode


class Solution:
    def findMaximumXOR(self, nums: list[int]) -> int:
        # Handle edge case
        if len(nums) < 2:
            return 0

        max_num = max(nums)
        L = max_num.bit_length() if max_num > 0 else 1

        # Build trie
        root = TrieNode()
        for num in nums:
            node = root
            for i in range(L - 1, -1, -1):
                bit = (num >> i) & 1
                if bit not in node.children:
                    node.children[bit] = TrieNode()
                node = node.children[bit]

        # Find max XOR
        max_xor = 0
        for num in nums:
            node = root
            curr_xor = 0
            for i in range(L - 1, -1, -1):
                bit = (num >> i) & 1
                want = 1 - bit

                if want in node.children:
                    curr_xor |= (1 << i)
                    node = node.children[want]
                else:
                    node = node.children[bit]

            max_xor = max(max_xor, curr_xor)

        return max_xor
```

### Optimized: Build and Query Simultaneously

```python
class Solution:
    def findMaximumXOR(self, nums: list[int]) -> int:
        """
        Optimization: Insert and query in one pass.
        For each num, query existing trie, then insert num.
        """
        max_num = max(nums)
        L = max_num.bit_length() if max_num > 0 else 1

        root = {}
        max_xor = 0

        for num in nums:
            # Query (only if trie is not empty)
            if root:
                node = root
                curr_xor = 0
                for i in range(L - 1, -1, -1):
                    bit = (num >> i) & 1
                    want = 1 - bit

                    if want in node:
                        curr_xor |= (1 << i)
                        node = node[want]
                    elif bit in node:
                        node = node[bit]
                    else:
                        break

                max_xor = max(max_xor, curr_xor)

            # Insert
            node = root
            for i in range(L - 1, -1, -1):
                bit = (num >> i) & 1
                if bit not in node:
                    node[bit] = {}
                node = node[bit]

        return max_xor
```

---

## Complexity Analysis

| Aspect | Complexity | Notes |
|--------|------------|-------|
| Time (build trie) | O(n × L) | L = max bit length (32 for int) |
| Time (query) | O(n × L) | Query for each of n numbers |
| Total Time | O(n × L) = O(n) | L is constant for 32-bit |
| Space | O(n × L) = O(n) | At most n × L nodes |

### Comparison with Brute Force

| Approach | Time | Space |
|----------|------|-------|
| Brute force (all pairs) | O(n²) | O(1) |
| Bitwise Trie | O(n × 32) = O(n) | O(n × 32) |

For n = 10^5, trie is ~3000x faster.

---

## Why This Works

### XOR Properties

```
XOR truth table:
0 XOR 0 = 0
0 XOR 1 = 1
1 XOR 0 = 1
1 XOR 1 = 0

To maximize XOR:
- For each bit position, having different bits gives 1
- Higher bits matter more (2^31 > sum of all lower bits)
- Greedily maximize from MSB to LSB
```

### Greedy Strategy

```
For number X, to find Y that maximizes X XOR Y:
1. Start from MSB (most significant bit)
2. If X has bit 0, we want Y to have bit 1 (and vice versa)
3. If desired bit doesn't exist in trie, take what's available
4. Each successful opposite bit adds 2^i to the XOR result
```

---

## Common Variations

### Maximum XOR With an Element From Array (LeetCode 1707)

```python
class Solution:
    def maximizeXor(self, nums: list[int], queries: list[list[int]]) -> list[int]:
        """
        queries[i] = [x_i, m_i]
        Return max(x_i XOR num) where num <= m_i

        Approach: Offline query processing
        1. Sort queries by m_i
        2. Sort nums
        3. For each query, add nums <= m_i to trie, then query
        """
        nums.sort()
        # (m_i, x_i, original_index)
        indexed_queries = sorted(
            [(m, x, i) for i, (x, m) in enumerate(queries)]
        )

        root = {}
        result = [-1] * len(queries)
        num_idx = 0

        for m, x, query_idx in indexed_queries:
            # Add all nums <= m to trie
            while num_idx < len(nums) and nums[num_idx] <= m:
                self._insert(root, nums[num_idx])
                num_idx += 1

            # Query if trie is not empty
            if root:
                result[query_idx] = self._query(root, x)

        return result

    def _insert(self, root, num):
        node = root
        for i in range(31, -1, -1):
            bit = (num >> i) & 1
            if bit not in node:
                node[bit] = {}
            node = node[bit]

    def _query(self, root, num):
        node = root
        xor_val = 0
        for i in range(31, -1, -1):
            bit = (num >> i) & 1
            want = 1 - bit
            if want in node:
                xor_val |= (1 << i)
                node = node[want]
            else:
                node = node[bit]
        return xor_val
```

### Maximum Genetic Difference Query (LeetCode 1938)

```python
def maxGeneticDifference(self, parents: list[int], queries: list[list[int]]) -> list[int]:
    """
    Tree structure, each node has value 0 to n-1.
    Query: Max XOR with any node on path from root to node_i.

    Approach: DFS with trie insert/remove
    """
    # Build tree
    from collections import defaultdict
    children = defaultdict(list)
    root = -1
    for i, p in enumerate(parents):
        if p == -1:
            root = i
        else:
            children[p].append(i)

    # Group queries by node
    node_queries = defaultdict(list)
    for i, (node, val) in enumerate(queries):
        node_queries[node].append((val, i))

    result = [0] * len(queries)
    trie = {}

    def insert(num):
        node = trie
        for i in range(17, -1, -1):
            bit = (num >> i) & 1
            if bit not in node:
                node[bit] = {'count': 0}
            node = node[bit]
            node['count'] += 1

    def remove(num):
        node = trie
        for i in range(17, -1, -1):
            bit = (num >> i) & 1
            node = node[bit]
            node['count'] -= 1

    def query(num):
        node = trie
        xor_val = 0
        for i in range(17, -1, -1):
            bit = (num >> i) & 1
            want = 1 - bit
            if want in node and node[want]['count'] > 0:
                xor_val |= (1 << i)
                node = node[want]
            else:
                node = node[bit]
        return xor_val

    def dfs(node_id):
        insert(node_id)
        # Answer queries for this node
        for val, query_idx in node_queries[node_id]:
            result[query_idx] = query(val)
        # Visit children
        for child in children[node_id]:
            dfs(child)
        remove(node_id)

    dfs(root)
    return result
```

### Count Pairs With XOR in Range (LeetCode 1803)

```python
def countPairs(self, nums: list[int], low: int, high: int) -> int:
    """
    Count pairs where low <= nums[i] XOR nums[j] <= high

    Approach: Count pairs with XOR < limit
    Answer = count(< high+1) - count(< low)
    """
    def count_less(limit):
        root = {}
        count = 0

        for num in nums:
            # Query: count pairs with XOR < limit
            node = root
            for i in range(14, -1, -1):
                if node is None:
                    break
                bit = (num >> i) & 1
                limit_bit = (limit >> i) & 1

                if limit_bit == 1:
                    # If limit has 1, XOR with same bit gives 0 (< 1)
                    # All numbers in that subtree are valid
                    if bit in node:
                        count += node[bit].get('cnt', 0)
                    # Continue with opposite bit (gives XOR = 1)
                    node = node.get(1 - bit)
                else:
                    # If limit has 0, must have XOR = 0, take same bit
                    node = node.get(bit)

            # Insert num into trie
            node = root
            for i in range(14, -1, -1):
                bit = (num >> i) & 1
                if bit not in node:
                    node[bit] = {'cnt': 0}
                node = node[bit]
                node['cnt'] += 1

        return count

    return count_less(high + 1) - count_less(low)
```

---

## Edge Cases

1. **Single element**: No pairs, return 0
2. **All same numbers**: XOR is 0
3. **Contains 0**: 0 XOR x = x
4. **Negative numbers**: Depends on problem; often use unsigned interpretation
5. **Empty array**: Return 0

---

## Interview Tips

1. **Start with brute force**: O(n²) all pairs approach
2. **Introduce XOR insight**: Explain that opposite bits maximize XOR
3. **Explain greedy MSB strategy**: Higher bits matter more
4. **Connect to trie**: Binary paths for bit positions
5. **Walk through example**: Show how the path selection works

---

## Step-by-Step Walkthrough

```
nums = [3, 10, 5, 25]

Build trie (using 5 bits):
  3 = 00011
  Insert: root -> 0 -> 0 -> 0 -> 1 -> 1

  10 = 01010
  Insert: root -> 0 -> 1 -> 0 -> 1 -> 0

  5 = 00101
  Insert: root -> 0 -> 0 -> 1 -> 0 -> 1

  25 = 11001
  Insert: root -> 1 -> 1 -> 0 -> 0 -> 1

Query for num = 5 (00101):
  Bit 4: have 0, want 1 → 1 exists → take 1, xor += 16
  Bit 3: have 0, want 1 → 1 exists → take 1, xor += 8
  Bit 2: have 1, want 0 → 0 exists → take 0, xor += 4
  Bit 1: have 0, want 1 → no 1, take 0, xor += 0
  Bit 0: have 1, want 0 → no 0, take 1, xor += 0

  XOR = 16 + 8 + 4 = 28 ✓

This matches 5 XOR 25:
  00101 XOR 11001 = 11100 = 28
```

---

## Practice Problems

| # | Problem | Difficulty | Key Concept |
|---|---------|------------|-------------|
| 1 | Maximum XOR of Two Numbers in an Array | Medium | Basic bitwise trie |
| 2 | Maximum XOR With an Element From Array | Hard | Offline queries + trie |
| 3 | Maximum Genetic Difference Query | Hard | DFS + dynamic trie |
| 4 | Count Pairs With XOR in a Range | Hard | Counting with trie |
| 5 | Maximum XOR After Operations | Medium | XOR properties + trie |

---

## Related Sections

- [Trie Implementation](./01-trie-implementation.md) - Basic trie concepts
- [Bit Manipulation](../15-bit-manipulation/README.md) - XOR properties
- [Binary Search](../10-binary-search/README.md) - Alternative approaches
