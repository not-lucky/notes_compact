# Maximum XOR of Two Numbers (Bitwise Trie)

[Previous: Autocomplete](./06-autocomplete.md) | [Next: Suffix Tries](./09-suffix-tries.md)

> **Prerequisites:** [Trie Implementation](./01-trie-implementation.md), [Bit Manipulation](../15-bit-manipulation/01-bitwise-operators.md)

## Quick Reference

| Operation | Complexity | Explanation |
| :--- | :--- | :--- |
| **Build Trie** | `O(N * L)` | Insert `N` numbers, each having `L` bits (usually 32 for integers) |
| **Max XOR Query** | `O(L)` | Greedily pick opposite bits from MSB to LSB for a single number |
| **Total Find Max XOR**| `O(N * L)` | Insert and query for `N` numbers |
| **Space Complexity** | `O(N * L)` | Trie nodes to store `N` numbers of `L` bits |

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
def xor_range(L: int, R: int) -> int:
    # XOR from 1 to n has a pattern based on n % 4
    def xor_1_to_n(n: int) -> int:
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
                /      \
              0          1
            /   \         \
           0     1         1
          / \     \         \
         0   1     0         0
         |   |     |         |
         1   0     1         0
         |   |     |         |
         1   1     0         1
        (3) (5)  (10)      (25)

For num=5 (00101), find max XOR:
  Bit 4: have 0, want 1 → take 1 (exists: 25's path)
  Bit 3: have 0, want 1 → take 1 (25 continues 1→1)
  Bit 2: have 1, want 0 → take 0 (25 continues 1→1→0)
  Bit 1: have 0, want 1 → no 1, forced to take 0
  Bit 0: have 1, want 0 → no 0, forced to take 1

  Path taken: 11001 = 25
  XOR: 5 ⊕ 25 = 00101 ⊕ 11001 = 11100 = 28 ✓
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
        root: dict[int, dict] = {}
        for num in nums:
            curr = root
            for i in range(L - 1, -1, -1):  # MSB to LSB
                bit = (num >> i) & 1
                if bit not in curr:
                    curr[bit] = {}
                curr = curr[bit]

        # Find max XOR for each number
        max_xor = 0
        for num in nums:
            curr = root
            curr_xor = 0
            for i in range(L - 1, -1, -1):
                bit = (num >> i) & 1
                want = 1 - bit  # Opposite bit

                if want in curr:
                    curr_xor |= (1 << i)  # This bit contributes to XOR
                    curr = curr[want]
                else:
                    curr = curr[bit]

            max_xor = max(max_xor, curr_xor)

        return max_xor
```

### With Explicit TrieNode Class

```python
class TrieNode:
    __slots__ = ('children',)

    def __init__(self) -> None:
        self.children: dict[int, 'TrieNode'] = {}  # 0 or 1 -> TrieNode


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

        root: dict[int, dict] = {}
        max_xor = 0

        for num in nums:
            # Query (only if trie is not empty)
            if root:
                curr = root
                curr_xor = 0
                for i in range(L - 1, -1, -1):
                    bit = (num >> i) & 1
                    want = 1 - bit

                    if want in curr:
                        curr_xor |= (1 << i)
                        curr = curr[want]
                    elif bit in curr:
                        curr = curr[bit]
                    else:
                        # Defensive: shouldn't happen with fully-inserted
                        # L-bit numbers, but guards against empty subtrees
                        break

                max_xor = max(max_xor, curr_xor)

            # Insert
            curr = root
            for i in range(L - 1, -1, -1):
                bit = (num >> i) & 1
                if bit not in curr:
                    curr[bit] = {}
                curr = curr[bit]

        return max_xor
```

---

## Complexity Analysis

| Aspect            | Complexity      | Notes                           |
| ----------------- | --------------- | ------------------------------- |
| Time (build trie) | O(n × L)        | L = max bit length (32 for int) |
| Time (query)      | O(n × L)        | Query for each of n numbers     |
| Total Time        | O(n × L) = O(n) | L is constant for 32-bit        |
| Space             | O(n × L) = O(n) | At most n × L nodes             |

### Comparison with Brute Force

| Approach                | Time             | Space     |
| ----------------------- | ---------------- | --------- |
| Brute force (all pairs) | O(n²)            | O(1)      |
| Bitwise Trie            | O(n × 32) = O(n) | O(n × 32) |

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
        3. For each query, incrementally add nums <= m_i to the Trie
        4. Query the Trie for max XOR. If the Trie is empty, return -1.
        """
        nums.sort()

        # (m_i, x_i, original_index)
        indexed_queries = sorted(
            [(m, x, i) for i, (x, m) in enumerate(queries)]
        )

        root: dict[int, dict] = {}
        ans = [-1] * len(queries)
        j = 0
        n = len(nums)

        for m, x, i in indexed_queries:
            while j < n and nums[j] <= m:
                self._insert(root, nums[j])
                j += 1

            if j > 0:
                ans[i] = self._query(root, x)

        return ans

    def _insert(self, root: dict, num: int) -> None:
        curr = root
        # 32 bits: problem constraints guarantee nums[i], x_i ≤ 10^9 < 2^30,
        # but using 32 bits is safe and standard for non-negative int problems.
        for i in range(31, -1, -1):
            bit = (num >> i) & 1
            if bit not in curr:
                curr[bit] = {}
            curr = curr[bit]

    def _query(self, root: dict, num: int) -> int:
        curr = root
        xor_val = 0
        for i in range(31, -1, -1):  # Must match bit width used in _insert
            bit = (num >> i) & 1
            want = 1 - bit

            if want in curr:
                xor_val |= (1 << i)
                curr = curr[want]
            else:
                curr = curr[bit]

        return xor_val
```

### Maximum Genetic Difference Query (LeetCode 1938)

```python
class Solution:
    def maxGeneticDifference(self, parents: list[int], queries: list[list[int]]) -> list[int]:
        """
        Tree structure, each node has value 0 to n-1.
        Query: Max XOR with any node on path from root to node_i.

        Approach: DFS with trie insert/remove
        """
        from collections import defaultdict

        children: dict[int, list[int]] = defaultdict(list)
        root = -1

        for i, p in enumerate(parents):
            if p == -1:
                root = i
            else:
                children[p].append(i)

        # Group queries by node
        node_queries: dict[int, list[tuple[int, int]]] = defaultdict(list)
        for i, (node, val) in enumerate(queries):
            node_queries[node].append((val, i))

        result = [0] * len(queries)
        # Trie nodes use int keys (0, 1) for children and str key ('count')
        trie: dict = {}

        def insert(num: int) -> None:
            curr = trie
            # 18 bits: n ≤ 10^5, val ≤ 2*10^5, so max value < 2^18 = 262144
            for i in range(17, -1, -1):
                bit = (num >> i) & 1
                if bit not in curr:
                    curr[bit] = {'count': 0}
                curr = curr[bit]
                curr['count'] += 1

        def remove(num: int) -> None:
            curr = trie
            for i in range(17, -1, -1):
                bit = (num >> i) & 1
                curr = curr[bit]
                curr['count'] -= 1

        def query(num: int) -> int:
            curr = trie
            xor_val = 0
            for i in range(17, -1, -1):
                bit = (num >> i) & 1
                want = 1 - bit
                if want in curr and curr[want]['count'] > 0:
                    xor_val |= (1 << i)
                    curr = curr[want]
                else:
                    curr = curr[bit]
            return xor_val

        def dfs(node_id: int) -> None:
            insert(node_id)

            for val, query_idx in node_queries[node_id]:
                result[query_idx] = query(val)

            for child in children[node_id]:
                dfs(child)

            remove(node_id)

        dfs(root)

        return result
```

### Count Pairs With XOR in Range (LeetCode 1803)

```python
class Solution:
    def countPairs(self, nums: list[int], low: int, high: int) -> int:
        """
        Count pairs where low <= nums[i] XOR nums[j] <= high

        Approach: Count pairs with XOR < limit
        Answer = count(< high+1) - count(< low)
        """
        def count_less(limit: int) -> int:
            # Trie nodes use int keys (0, 1) for children and str key ('cnt')
            root: dict = {}
            count = 0

            for num in nums:
                node: dict | None = root
                # 15 bits: nums[i] ≤ 2*10^4 < 2^15 = 32768
                for i in range(14, -1, -1):
                    if node is None:
                        break

                    bit = (num >> i) & 1
                    limit_bit = (limit >> i) & 1

                    if limit_bit == 1:
                        # If limit_bit is 1, choosing the SAME bit yields XOR bit 0 (< 1).
                        # The ENTIRE subtree for this path is strictly less than the limit.
                        if bit in node:
                            count += node[bit].get('cnt', 0)

                        # To try to match the limit_bit of 1, we must choose the OPPOSITE bit.
                        node = node.get(1 - bit)
                    else:
                        # If limit_bit is 0, we must choose the SAME bit to get XOR bit 0 (== 0).
                        # Any other choice would exceed the limit.
                        node = node.get(bit)

                # Insert num into trie
                curr = root
                for i in range(14, -1, -1):
                    bit = (num >> i) & 1
                    if bit not in curr:
                        curr[bit] = {'cnt': 0}
                    curr = curr[bit]
                    curr['cnt'] += 1

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

Let's break down how we find the maximum XOR for $5$ against the array $[3, 10, 5, 25]$ using a 5-bit representation ($L = 5$).

**Array:**
- $3 = 00011_2$
- $10 = 01010_2$
- $5 = 00101_2$
- $25 = 11001_2$

**Goal:** Maximize $5 \oplus Y$ for $Y \in \text{Array}$. We process bits from MSB (bit 4) to LSB (bit 0).
The bit values at each index $i$ contribute $2^i$ to the final XOR.

**For $X = 5$ ($00101_2$):**

| Bit ($i$) | X's Bit | Want (1 - X) | Available Paths in Trie? | Action | Chosen Path Bit | XOR Contribution | Running Total |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **4** ($2^4=16$) | $0$ | $1$ | Yes ($25$'s path starts with 1) | Take 1 | $1$ | $16$ | $16$ |
| **3** ($2^3=8$) | $0$ | $1$ | Yes ($25$ continues `1 -> 1`) | Take 1 | $1$ | $8$ | $24$ |
| **2** ($2^2=4$) | $1$ | $0$ | Yes ($25$ continues `1 -> 1 -> 0`) | Take 0 | $0$ | $4$ | $28$ |
| **1** ($2^1=2$) | $0$ | $1$ | No ($25$ continues `.. -> 0`, no `1`) | Forced 0 | $0$ | $0$ | $28$ |
| **0** ($2^0=1$) | $1$ | $0$ | No ($25$ ends in `1`, no `0`) | Forced 1 | $1$ | $0$ | $28$ |

**Result:**
The path taken in the Trie corresponds to $11001_2 = 25$.
Maximum XOR: $5 \oplus 25 = 28$.

**Understanding the `max_num.bit_length()` Optimization:**
Instead of hardcoding $L = 32$ for standard integers, we find the maximum number in the array, `max_num`. The highest set bit in `max_num` determines the maximum number of bits needed to represent any number in the array. Thus, `L = max_num.bit_length()` avoids adding leading zeroes to our Trie, saving space and reducing time complexity to effectively $O(N \cdot L)$, where $L \ll 32$.

---

## Practice Problems

| #   | Problem                                | Difficulty | Key Concept            | LeetCode |
| --- | -------------------------------------- | ---------- | ---------------------- | -------- |
| 1   | Maximum XOR of Two Numbers in an Array | Medium     | Basic bitwise trie     | [421](https://leetcode.com/problems/maximum-xor-of-two-numbers-in-an-array/) |
| 2   | Maximum XOR After Operations           | Medium     | XOR properties + trie  | [2317](https://leetcode.com/problems/maximum-xor-after-operations-on-an-array/) |
| 3   | Maximum XOR With an Element From Array | Hard       | Offline queries + trie | [1707](https://leetcode.com/problems/maximum-xor-with-an-element-from-array/) |
| 4   | Count Pairs With XOR in a Range        | Hard       | Counting with trie     | [1803](https://leetcode.com/problems/count-pairs-with-xor-in-a-range/) |
| 5   | Maximum Genetic Difference Query       | Hard       | DFS + dynamic trie     | [1938](https://leetcode.com/problems/maximum-genetic-difference-query/) |

---

## Related Sections

- [Trie Implementation](./01-trie-implementation.md) - Basic trie concepts
- [Bit Manipulation](../15-bit-manipulation/README.md) - XOR properties
- [Binary Search](../10-binary-search/README.md) - Alternative approaches
