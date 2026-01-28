# Top-K Pattern

> **Prerequisites:** [02-python-heapq](./02-python-heapq.md)

## Interview Context

The Top-K pattern is a FANG+ interview staple because:

1. **Frequency**: Appears in ~30% of heap-related interviews
2. **Efficiency test**: Shows you understand O(n log k) vs O(n log n)
3. **Variations**: Largest, smallest, frequent, closest — same pattern
4. **Follow-ups**: Interviewers love asking "what if k changes?" or "what if data streams?"

Mastering this pattern unlocks many medium-difficulty problems.

---

## Building Intuition

**Why Use the OPPOSITE Heap Type?**

This is the most counterintuitive part. Let's think about it step by step:

```
Goal: Find 3 LARGEST from [5, 3, 8, 1, 9, 2, 7]

Naive thought: "I want largest, so use max heap?"
Problem: Max heap of ALL n elements + pop 3 = O(n + 3 log n) space O(n)

Better: Keep only 3 candidates, evict the WORST candidate when we find better.

Key insight: What makes a candidate "worst" for "3 largest"?
→ The SMALLEST of the candidates! (It's the one least deserving of being in top 3)

So we need quick access to the SMALLEST of our k candidates
→ MIN heap of size k!
```

**Mental Model: The VIP List**

Imagine you're a bouncer with a VIP list that can only hold k people. You track "net worth" (higher = more VIP).

```
VIP list capacity: 3
Current VIPs: [$5M, $8M, $10M]

New person arrives: $12M
Who do you kick out? The POOREST current VIP ($5M)!

You need quick access to the poorest VIP → min heap by net worth
```

For "k poorest people" (k smallest), you'd kick out the RICHEST → max heap.

**The Eviction Rule Made Simple**

```
Finding K largest:
- New candidate vs SMALLEST current candidate
- If new > smallest: evict smallest, add new
- Need quick access to smallest → MIN heap

Finding K smallest:
- New candidate vs LARGEST current candidate
- If new < largest: evict largest, add new
- Need quick access to largest → MAX heap

The heap root is ALWAYS what you might evict!
```

**Why Size K and Not Size N?**

```
Size N heap + k pops:  O(n + k log n) time, O(n) space
Size K heap:           O(n log k) time,    O(k) space

When k << n:
- n log k << n log n (less work per element)
- O(k) << O(n) (less space)

When k ≈ n:
- Just sort the array instead!
```

**Visual: The Heap as a "Threshold Keeper"**

```
Finding 3 largest from stream: [5, 3, 8, 1, 9, 2, 7]

MIN heap of size 3, root = "entry threshold"

[5]         threshold=5 (only one so far)
[3,5]       threshold=3
[3,5,8]     threshold=3 (heap full)
1 < 3?      Yes, skip (not good enough)
9 > 3?      Yes, evict 3, add 9 → [5,8,9], threshold=5
2 < 5?      Yes, skip
7 > 5?      Yes, evict 5, add 7 → [7,8,9], threshold=7

Final threshold=7, heap contains [7,8,9] = 3 largest
```

---

## When NOT to Use Top-K with Heap

**1. K Is Close to N**

When k ≈ n, just sort:

```python
# If k > n/2, sorting is often faster
# O(n log n) sort vs O(n log k) heap... when k = n/2: same complexity!

# Rule of thumb:
if k > len(nums) // 2:
    return sorted(nums, reverse=True)[:k]
```

**2. You Only Need the Kth Element (Not All K)**

If you just need the single kth value, not all k values:

```python
# Top-K heap gives all k elements: O(n log k)
# QuickSelect gives just kth element: O(n) average

# For single value, QuickSelect is faster
```

**3. Data Needs to Be Updated Dynamically**

Heap doesn't efficiently support:

```python
# "Remove element X from top-K"
# "Update element X's value"

# These require O(n) search + O(log n) reheapify
# Consider: indexed heap or balanced BST instead
```

**4. You Need Sorted Order Immediately**

Heap doesn't maintain full sorted order:

```python
heap = [3, 5, 4]  # Valid min heap, but not sorted!

# To get sorted top-K:
# Option 1: sort the heap result O(k log k)
# Option 2: pop k times O(k log k)
# heapq.nlargest already returns sorted!
```

**5. K = 1 (Just Min or Max)**

Don't use heap for finding single min or max:

```python
# Overkill:
heapq.nlargest(1, nums)[0]  # O(n log 1) = O(n), but with overhead

# Simple:
max(nums)  # O(n), less overhead
```

**Red Flags:**

- "K is greater than half the array" → Just sort
- "Need only the kth value, not all k" → QuickSelect
- "Elements change after initial query" → Need different structure
- "K is 1" → Use min()/max()

---

## Core Insight: Which Heap for Which Problem?

This is **the most common mistake** in heap interviews:

| Problem             | Heap Type    | Size | Why                         |
| ------------------- | ------------ | ---- | --------------------------- |
| K **largest**       | **Min** heap | K    | Evict smallest of the large |
| K **smallest**      | **Max** heap | K    | Evict largest of the small  |
| K **most** frequent | **Min** heap | K    | Evict least frequent        |
| K **closest**       | **Max** heap | K    | Evict furthest              |

**The Rule**: Use the **opposite** heap type. The heap root is what you might evict.

---

## Visual Example: K Largest

Finding 3 largest from `[5, 3, 8, 1, 9, 2, 7]`:

```
Use MIN heap of size 3 (root = smallest of the largest)

Process 5: heap = [5]           size < 3, just add
Process 3: heap = [3, 5]        size < 3, just add
Process 8: heap = [3, 5, 8]     size = 3
Process 1: 1 < 3 (root)         skip (too small)
Process 9: 9 > 3 (root)         replace 3 with 9: [5, 8, 9]
Process 2: 2 < 5 (root)         skip
Process 7: 7 > 5 (root)         replace 5 with 7: [7, 8, 9]

Final: [7, 8, 9] are the 3 largest
```

---

## Pattern Template: K Largest

```python
import heapq

def k_largest(nums: list[int], k: int) -> list[int]:
    """
    Find k largest elements.

    Time: O(n log k)
    Space: O(k)

    Strategy: Min heap of size k. Root is smallest of the largest.
    If new element > root, it deserves to be in top k, so replace root.
    """
    if k <= 0:
        return []
    if k >= len(nums):
        return nums[:]

    # Min heap of size k
    heap = nums[:k]
    heapq.heapify(heap)

    for num in nums[k:]:
        if num > heap[0]:  # Larger than smallest in heap
            heapq.heapreplace(heap, num)

    return heap  # Unordered k largest

def k_largest_sorted(nums: list[int], k: int) -> list[int]:
    """Return k largest in descending order."""
    return sorted(k_largest(nums, k), reverse=True)
```

---

## Pattern Template: K Smallest

```python
import heapq

def k_smallest(nums: list[int], k: int) -> list[int]:
    """
    Find k smallest elements.

    Time: O(n log k)
    Space: O(k)

    Strategy: Max heap of size k (negate values).
    Root is largest of the smallest.
    """
    if k <= 0:
        return []
    if k >= len(nums):
        return nums[:]

    # Max heap (negated) of size k
    heap = [-x for x in nums[:k]]
    heapq.heapify(heap)

    for num in nums[k:]:
        if num < -heap[0]:  # Smaller than largest in heap
            heapq.heapreplace(heap, -num)

    return [-x for x in heap]  # Unordered k smallest
```

---

## Using heapq.nlargest / nsmallest

For simple cases, use built-in functions:

```python
import heapq

nums = [5, 3, 8, 1, 9, 2, 7]

# K largest
largest = heapq.nlargest(3, nums)  # [9, 8, 7]

# K smallest
smallest = heapq.nsmallest(3, nums)  # [1, 2, 3]

# With key function
words = ['apple', 'pie', 'strawberry', 'fig']
longest = heapq.nlargest(2, words, key=len)  # ['strawberry', 'apple']
```

---

## Variation 1: Top K Frequent Elements

```python
import heapq
from collections import Counter

def top_k_frequent(nums: list[int], k: int) -> list[int]:
    """
    Find k most frequent elements.

    Time: O(n log k) - counting is O(n), heap is O(n log k)
    Space: O(n) for counter

    Example: nums = [1,1,1,2,2,3], k = 2 → [1, 2]
    """
    # Count frequencies
    count = Counter(nums)

    # Method 1: nlargest with key
    return heapq.nlargest(k, count.keys(), key=count.get)

    # Method 2: Manual heap (for understanding)
    # Min heap of (freq, num), size k
    # heap = []
    # for num, freq in count.items():
    #     heapq.heappush(heap, (freq, num))
    #     if len(heap) > k:
    #         heapq.heappop(heap)
    # return [num for freq, num in heap]
```

---

## Variation 2: K Closest Points to Origin

```python
import heapq

def k_closest(points: list[list[int]], k: int) -> list[list[int]]:
    """
    Find k closest points to origin (0, 0).

    Time: O(n log k)
    Space: O(k)

    Use MAX heap of size k: evict furthest point.
    """
    # Max heap: (-distance, point)
    heap = []

    for x, y in points:
        dist = x*x + y*y  # No need for sqrt (monotonic)

        if len(heap) < k:
            heapq.heappush(heap, (-dist, [x, y]))
        elif dist < -heap[0][0]:  # Closer than furthest in heap
            heapq.heapreplace(heap, (-dist, [x, y]))

    return [point for _, point in heap]
```

---

## Variation 3: Top K in Data Stream

```python
import heapq

class KthLargest:
    """
    Find kth largest in stream of numbers.

    Time: O(log k) per add
    Space: O(k)

    Maintain min heap of size k.
    Root is always the kth largest.
    """
    def __init__(self, k: int, nums: list[int]):
        self.k = k
        self.heap = nums[:]
        heapq.heapify(self.heap)

        # Reduce to size k
        while len(self.heap) > k:
            heapq.heappop(self.heap)

    def add(self, val: int) -> int:
        """Add value and return kth largest."""
        if len(self.heap) < self.k:
            heapq.heappush(self.heap, val)
        elif val > self.heap[0]:
            heapq.heapreplace(self.heap, val)

        return self.heap[0]


# Usage
kth = KthLargest(3, [4, 5, 8, 2])
# heap = [4, 5, 8] (size 3, smallest = 4 = 3rd largest)

kth.add(3)   # heap = [4, 5, 8], returns 4
kth.add(5)   # heap = [5, 5, 8], returns 5
kth.add(10)  # heap = [5, 8, 10], returns 5
kth.add(9)   # heap = [8, 9, 10], returns 8
```

---

## Variation 4: K Largest with Duplicates Counted Once

```python
import heapq

def k_largest_unique(nums: list[int], k: int) -> list[int]:
    """
    Find k largest unique elements.

    Time: O(n log k)
    Space: O(n) for set
    """
    unique = list(set(nums))
    return heapq.nlargest(k, unique)
```

---

## Complexity Analysis

| Approach           | Time       | Space | When to Use              |
| ------------------ | ---------- | ----- | ------------------------ |
| Sort + slice       | O(n log n) | O(n)  | k ≈ n                    |
| Heap of size k     | O(n log k) | O(k)  | k << n                   |
| nlargest/nsmallest | O(n log k) | O(k)  | Simple cases             |
| QuickSelect        | O(n) avg   | O(1)  | Only need kth, not all k |

**Break-even point**: When k ≈ n/log(n), heap and sort are similar.

---

## Common Mistakes

```python
import heapq

# WRONG: Using max heap for k largest
def k_largest_wrong(nums, k):
    heap = [-x for x in nums]  # Max heap of ALL elements
    heapq.heapify(heap)
    return [-heapq.heappop(heap) for _ in range(k)]
    # Time: O(n + k log n) - inefficient for large n, small k

# CORRECT: Use min heap of size k
def k_largest_correct(nums, k):
    return heapq.nlargest(k, nums)
    # Time: O(n log k)


# WRONG: Forgetting to handle k > n
def k_largest_no_check(nums, k):
    heap = nums[:k]  # Works
    heapq.heapify(heap)
    for num in nums[k:]:  # Might be empty
        if num > heap[0]:
            heapq.heapreplace(heap, num)
    return heap
    # If k > n, returns all nums (often correct but check problem)

# WRONG: Returning unsorted when sorted is expected
def k_largest_unsorted(nums, k):
    return heapq.nlargest(k, nums)  # Already returns sorted!
    # nlargest returns descending, nsmallest returns ascending
```

---

## Edge Cases

```python
# 1. k = 0
k_largest([1, 2, 3], 0)  # → []

# 2. k > len(nums)
k_largest([1, 2], 5)  # → [1, 2] or [2, 1]

# 3. k = len(nums)
k_largest([1, 2, 3], 3)  # → [1, 2, 3] (all elements)

# 4. All same elements
k_largest([5, 5, 5, 5], 2)  # → [5, 5]

# 5. Negative numbers
k_largest([-5, -1, -3], 2)  # → [-1, -3]

# 6. Empty array
k_largest([], 3)  # → []
```

---

## Interview Tips

1. **Ask about order**: Does result need to be sorted?
2. **Clarify k**: Can k be 0? Greater than array length?
3. **Explain heap choice**: "I use min heap because root is smallest of the largest"
4. **Mention complexity**: O(n log k) is better than O(n log n) when k << n
5. **Consider QuickSelect**: For kth element only, O(n) average is possible

---

## Practice Problems

| #   | Problem                         | Difficulty | Key Variation           |
| --- | ------------------------------- | ---------- | ----------------------- |
| 1   | Kth Largest Element in an Array | Medium     | Basic top-k             |
| 2   | Top K Frequent Elements         | Medium     | Frequency + heap        |
| 3   | K Closest Points to Origin      | Medium     | Distance-based          |
| 4   | Kth Largest Element in a Stream | Easy       | Streaming top-k         |
| 5   | Top K Frequent Words            | Medium     | Ties + alphabetical     |
| 6   | Sort Characters By Frequency    | Medium     | Frequency counting      |
| 7   | K Closest Elements              | Medium     | Two approaches possible |

---

## Key Takeaways

1. **K largest → Min heap of size K**: Root is what we might evict
2. **K smallest → Max heap of size K**: Same logic, opposite direction
3. **Time is O(n log k)**: Better than O(n log n) sorting when k is small
4. **heapq.nlargest/nsmallest**: Use for simple cases
5. **Stream variant**: Maintain heap of size k, root is the answer

---

## Next: [04-kth-largest-element.md](./04-kth-largest-element.md)

Deep dive into finding the kth largest element, including QuickSelect.
