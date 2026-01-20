# Kth Largest Element

> **Prerequisites:** [03-top-k-pattern](./03-top-k-pattern.md)

## Interview Context

"Find the kth largest element" is a classic because:

1. **Multiple solutions**: Heap, sorting, QuickSelect — tests depth of knowledge
2. **Follow-up potential**: "Can you do better than O(n log n)?"
3. **Real applications**: Database queries, percentile calculations
4. **Complexity analysis**: Shows understanding of average vs worst case

Interviewers often start with heap, then ask about QuickSelect.

---

## Building Intuition

**What Does "Kth Largest" Actually Mean?**

```
Array: [3, 2, 1, 5, 6, 4]
Sorted descending: [6, 5, 4, 3, 2, 1]
                    1st 2nd 3rd 4th 5th 6th largest

k=2 → 5 (second position in descending order)

Alternative view:
Sorted ascending: [1, 2, 3, 4, 5, 6]
                   0  1  2  3  4  5  ← indices

kth largest = element at index (n - k) when sorted ascending
k=2, n=6 → index 4 → value 5 ✓
```

**Why Min Heap of Size K Works**

Imagine a competition where only k winners advance:

```
Top 3 competition, contestants arrive one by one:

[3] → Qualify (only 1 so far)
[3,2] → Both qualify (only 2 so far)
[3,2,1] → All qualify (exactly 3 now)
[5] arrives, beats current worst (1) → [3,2,5]
[6] arrives, beats current worst (2) → [3,5,6]
[4] arrives, beats current worst (3) → [4,5,6]

Final 3: [4,5,6]
Kth (3rd) largest = smallest of the 3 = 4 ← That's the root!
```

The heap root is always the "weakest winner" — the kth largest.

**QuickSelect: Partial Sorting Insight**

QuickSelect asks: "What if we could stop sorting early?"

```
Full QuickSort: Partition everything, recurse both sides, O(n log n)
QuickSelect: Partition, but only recurse ONE side, O(n)

Why one side? After partitioning:
[elements < pivot] [pivot] [elements > pivot]
         left                    right

If pivot lands at index k-1, we're done!
If pivot is left of target, search right.
If pivot is right of target, search left.

We halve the problem each time (on average):
n + n/2 + n/4 + ... = 2n = O(n)
```

**Mental Model: Finding Median Height in a Crowd**

Imagine finding the 5th tallest person among 100 people.

**Sorting approach**: Line everyone up by height, count to 5th. (O(n log n))

**Heap approach**: Keep a "short list" of 5 tallest seen so far. Anyone taller than the shortest on your list gets swapped in. At the end, the shortest on your list is the answer. (O(n log k))

**QuickSelect approach**: Ask everyone to stand left/right of a random person. Count how many are taller. Repeat only with the relevant group. (O(n) average)

**When Each Approach Wins**

```
Sorting O(n log n):
- Simple, stable, no surprises
- Good when k ≈ n (need most of the array)
- Works well with sorted input

Heap O(n log k):
- Excellent when k << n
- Natural for streaming data
- Easy to implement correctly

QuickSelect O(n) average:
- Best single-query performance
- Modifies the array (usually OK)
- O(n²) worst case needs random pivot
```

---

## When NOT to Use Each Approach

**Don't Use Sorting When:**

```python
# K is very small relative to N
# O(n log n) is overkill for finding single element

nums = list(range(1000000))
k = 5
sorted(nums)[-k]  # Sorts 1M elements to find 5th largest!
```

**Don't Use Heap When:**

```python
# K = 1 (just use max())
max(nums)  # O(n), simpler than heap

# K ≈ N (sorting is similar or better)
# O(n log k) ≈ O(n log n) when k ≈ n

# You can't modify data and need O(n) time
# Heap is O(n log k), not O(n)
```

**Don't Use QuickSelect When:**

```python
# 1. Array can't be modified (QuickSelect partitions in-place)
# 2. Need worst-case guarantee (O(n²) possible without median-of-medians)
# 3. Data is streaming (can't partition what you haven't seen)
# 4. Need multiple different k values (re-run for each k)
```

**Red Flags:**
- "Array is read-only" → Can't use QuickSelect without copy
- "Need guaranteed O(n)" → QuickSelect is O(n) average, not worst
- "Data arrives as stream" → Heap is the answer
- "Need k=1" → Just use max()/min()

---

## Problem Statement

Given an integer array `nums` and integer `k`, return the **kth largest** element.

Note: It is the kth largest in **sorted order**, not the kth distinct element.

```
Example 1: nums = [3,2,1,5,6,4], k = 2 → 5
Sorted: [6,5,4,3,2,1], 2nd largest = 5

Example 2: nums = [3,2,3,1,2,4,5,5,6], k = 4 → 4
Sorted: [6,5,5,4,3,3,2,2,1], 4th largest = 4
```

---

## Approach 1: Sorting

```python
def find_kth_largest_sort(nums: list[int], k: int) -> int:
    """
    Sort and return kth from end.

    Time: O(n log n)
    Space: O(n) for sorted copy, or O(1) if in-place
    """
    nums.sort(reverse=True)
    return nums[k - 1]

    # Or without modifying input:
    # return sorted(nums, reverse=True)[k - 1]
```

Simple but not optimal for large n with small k.

---

## Approach 2: Min Heap of Size K (Optimal for Streaming)

```python
import heapq

def find_kth_largest_heap(nums: list[int], k: int) -> int:
    """
    Maintain min heap of k largest elements.
    Root is the kth largest.

    Time: O(n log k)
    Space: O(k)
    """
    # Build heap from first k elements
    heap = nums[:k]
    heapq.heapify(heap)

    # Process remaining elements
    for num in nums[k:]:
        if num > heap[0]:
            heapq.heapreplace(heap, num)

    return heap[0]  # Root is kth largest
```

**Why min heap?**
- We keep k largest elements
- Root is the smallest of these k
- Smallest of k largest = kth largest

---

## Approach 3: QuickSelect (Optimal Average Case)

QuickSelect is like QuickSort but only recurses into one partition.

```python
import random

def find_kth_largest_quickselect(nums: list[int], k: int) -> int:
    """
    QuickSelect algorithm.

    Time: O(n) average, O(n²) worst case
    Space: O(1) excluding recursion stack

    Convert to (n-k+1)th smallest for easier implementation.
    """
    # kth largest = (n-k+1)th smallest = element at index (n-k) when sorted
    target_index = len(nums) - k

    def quickselect(left: int, right: int) -> int:
        if left == right:
            return nums[left]

        # Random pivot to avoid O(n²) worst case
        pivot_idx = random.randint(left, right)
        pivot_idx = partition(left, right, pivot_idx)

        if pivot_idx == target_index:
            return nums[pivot_idx]
        elif pivot_idx < target_index:
            return quickselect(pivot_idx + 1, right)
        else:
            return quickselect(left, pivot_idx - 1)

    def partition(left: int, right: int, pivot_idx: int) -> int:
        pivot = nums[pivot_idx]
        # Move pivot to end
        nums[pivot_idx], nums[right] = nums[right], nums[pivot_idx]

        store_idx = left
        for i in range(left, right):
            if nums[i] < pivot:
                nums[i], nums[store_idx] = nums[store_idx], nums[i]
                store_idx += 1

        # Move pivot to final position
        nums[store_idx], nums[right] = nums[right], nums[store_idx]
        return store_idx

    return quickselect(0, len(nums) - 1)
```

---

## QuickSelect Visual Example

Finding 2nd largest in `[3, 2, 1, 5, 6, 4]`:
- 2nd largest = element at index 4 (0-indexed) when sorted ascending

```
Initial: [3, 2, 1, 5, 6, 4], target_index = 4

Round 1: pivot = 3
After partition: [2, 1, 3, 5, 6, 4]
                        ^ pivot at index 2
target_index (4) > 2, recurse right: [5, 6, 4]

Round 2: pivot = 5 (from subarray [5, 6, 4] which is indices 3-5)
After partition: [4, 5, 6]
                    ^ pivot at index 4
target_index (4) == 4, return nums[4] = 5 ✓
```

---

## Approach 4: Max Heap (Pop K Times)

```python
import heapq

def find_kth_largest_maxheap(nums: list[int], k: int) -> int:
    """
    Build max heap, pop k times.

    Time: O(n + k log n) = O(n) when k is small
    Space: O(n) for heap
    """
    # Negate for max heap
    max_heap = [-x for x in nums]
    heapq.heapify(max_heap)

    for _ in range(k - 1):
        heapq.heappop(max_heap)

    return -max_heap[0]
```

Less efficient than min heap approach when k << n.

---

## Comparison of Approaches

| Approach | Time (Average) | Time (Worst) | Space | Best When |
|----------|----------------|--------------|-------|-----------|
| Sort | O(n log n) | O(n log n) | O(n) | k ≈ n |
| Min Heap K | O(n log k) | O(n log k) | O(k) | k << n, streaming |
| Max Heap N | O(n + k log n) | O(n + k log n) | O(n) | k is very small |
| QuickSelect | O(n) | O(n²) | O(1)* | Single query |

*O(log n) for recursion stack in practice

**Recommendation:**
- Interview: Start with heap O(n log k), mention QuickSelect O(n)
- Production: QuickSelect for single query, heap for streaming

---

## Iterative QuickSelect (No Recursion)

```python
import random

def find_kth_largest_iterative(nums: list[int], k: int) -> int:
    """
    Iterative QuickSelect.

    Time: O(n) average
    Space: O(1)
    """
    target = len(nums) - k
    left, right = 0, len(nums) - 1

    while left <= right:
        pivot_idx = random.randint(left, right)
        pivot = nums[pivot_idx]

        # Move pivot to end
        nums[pivot_idx], nums[right] = nums[right], nums[pivot_idx]

        store = left
        for i in range(left, right):
            if nums[i] < pivot:
                nums[i], nums[store] = nums[store], nums[i]
                store += 1

        nums[store], nums[right] = nums[right], nums[store]

        if store == target:
            return nums[store]
        elif store < target:
            left = store + 1
        else:
            right = store - 1

    return nums[left]
```

---

## Using Python's heapq.nlargest

```python
import heapq

def find_kth_largest_nlargest(nums: list[int], k: int) -> int:
    """
    Use heapq.nlargest.

    Time: O(n log k)
    Space: O(k)
    """
    return heapq.nlargest(k, nums)[-1]
```

Clean and readable. Internally uses a heap.

---

## Variation: Kth Smallest

Same problem, just use different index or heap type:

```python
import heapq

def find_kth_smallest(nums: list[int], k: int) -> int:
    """Find kth smallest element."""
    return heapq.nsmallest(k, nums)[-1]

    # Or with max heap of size k:
    # heap = [-x for x in nums[:k]]
    # heapq.heapify(heap)
    # for num in nums[k:]:
    #     if num < -heap[0]:
    #         heapq.heapreplace(heap, -num)
    # return -heap[0]
```

---

## Edge Cases

```python
# 1. k = 1 (find maximum)
find_kth_largest([3, 1, 4], 1)  # → 4

# 2. k = n (find minimum)
find_kth_largest([3, 1, 4], 3)  # → 1

# 3. Duplicates
find_kth_largest([3, 3, 3, 3], 2)  # → 3

# 4. Negative numbers
find_kth_largest([-1, -2, -3], 1)  # → -1

# 5. Single element
find_kth_largest([5], 1)  # → 5

# 6. Already sorted
find_kth_largest([1, 2, 3, 4, 5], 3)  # → 3
```

---

## Interview Tips

1. **Start with heap**: O(n log k), easy to implement correctly
2. **Mention QuickSelect**: Show you know O(n) is possible
3. **Discuss trade-offs**: QuickSelect modifies array, has O(n²) worst case
4. **Random pivot**: Essential for QuickSelect to avoid worst case
5. **Clarify kth**: Is it 0-indexed or 1-indexed? Largest or smallest?

---

## Common Follow-up Questions

**Q: Can you do better than O(n log k)?**
A: Yes, QuickSelect is O(n) average.

**Q: What if array is streaming?**
A: Heap is better because we process one element at a time.

**Q: What if k changes frequently?**
A: Maintain sorted structure (balanced BST) or recalculate.

**Q: What if we need kth largest in multiple subarrays?**
A: Consider segment tree or wavelet tree (advanced).

---

## Practice Problems

| # | Problem | Difficulty | Key Variation |
|---|---------|------------|---------------|
| 1 | Kth Largest Element in an Array | Medium | Core problem |
| 2 | Kth Smallest Element in a Sorted Matrix | Medium | Matrix variation |
| 3 | Find K Pairs with Smallest Sums | Medium | Two arrays |
| 4 | Kth Smallest Element in a BST | Medium | Tree variation |
| 5 | Third Maximum Number | Easy | Handle duplicates |

---

## Key Takeaways

1. **Heap O(n log k)**: Min heap of size k, root is answer
2. **QuickSelect O(n)**: Partition-based, like QuickSort but one side
3. **Random pivot**: Critical for QuickSelect performance
4. **kth largest = (n-k+1)th smallest**: Index conversion trick
5. **Interview strategy**: Heap first, then discuss QuickSelect

---

## Next: [05-merge-k-sorted.md](./05-merge-k-sorted.md)

Learn to merge K sorted lists/arrays using heaps.
