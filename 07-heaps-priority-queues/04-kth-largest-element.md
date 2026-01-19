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
