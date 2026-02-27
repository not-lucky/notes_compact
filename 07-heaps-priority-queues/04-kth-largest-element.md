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

Imagine a competition where only $k$ winners advance:

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

The heap root is always the "weakest winner" — the $k$-th largest.

**QuickSelect: Partial Sorting Insight**

QuickSelect asks: "What if we could stop sorting early?"

```
Full QuickSort: Partition everything, recurse both sides, O(n log n)
QuickSelect: Partition, but only recurse ONE side, O(n) average

Why one side? After partitioning:
[elements < pivot] [pivot] [elements > pivot]
         left                    right

If pivot lands at index k-1, we're done!
If pivot is left of target, search right.
If pivot is right of target, search left.

We halve the problem size each time (on average):
n + n/2 + n/4 + ... ≈ 2n = O(n)
```

**Mental Model: Finding Median Height in a Crowd**

Imagine finding the 5th tallest person among 100 people.

**Sorting approach**: Line everyone up by height, count to 5th. ($O(n \log n)$)
**Heap approach**: Keep a "short list" of 5 tallest seen so far. Anyone taller than the shortest on your list gets swapped in. At the end, the shortest on your list is the answer. ($O(n \log k)$)
**QuickSelect approach**: Ask everyone to stand left or right of a randomly chosen person based on height. Count how many are taller. If there are exactly 4 people taller, your random person is the answer! Otherwise, repeat only with the relevant group. ($O(n)$ average)

---

## When NOT to Use Each Approach

**Don't Use Sorting When:**

```python
# K is very small relative to N
# O(n log n) is overkill for finding a single element

nums = list(range(1000000))
k = 5
sorted(nums)[-k]  # Sorts 1M elements to find 5th largest!
```

**Don't Use Heap When:**

```python
# K = 1 (just use max())
max(nums)  # O(n), simpler and faster than heap

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
- "Need guaranteed O(n)" → QuickSelect is $O(n)$ average, not worst (median-of-medians provides guaranteed $O(n)$ but is rarely practical to implement)
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

Simple, readable, but not optimal for large $n$ with small $k$.

---

## Approach 2: Min Heap of Size K (Optimal for Streaming)

**Why min heap?**
- We want to keep the $k$ largest elements
- The root of a min heap is the smallest of these $k$
- The smallest of the $k$ largest = the $k$-th largest

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

---

## Approach 3: QuickSelect (Optimal Average Case)

QuickSelect is like QuickSort but only recurses into one partition.

```python
import random

def find_kth_largest_quickselect(nums: list[int], k: int) -> int:
    """
    QuickSelect algorithm (Recursive).

    Time: O(n) average, O(n²) worst case
    Space: O(log n) average for recursion stack

    Convert to (n-k) index for easier implementation (finding the element 
    that would be at index n-k if the array was sorted ascending).
    """
    target_index = len(nums) - k

    def quickselect(left: int, right: int) -> int:
        # Base case: subarray with 1 element
        if left == right:
            return nums[left]

        # Random pivot to avoid O(n²) worst case on sorted arrays
        pivot_idx = random.randint(left, right)
        pivot = nums[pivot_idx]

        # Move pivot to end
        nums[pivot_idx], nums[right] = nums[right], nums[pivot_idx]

        # Lomuto Partition Scheme
        store_idx = left
        for i in range(left, right):
            if nums[i] < pivot:
                nums[i], nums[store_idx] = nums[store_idx], nums[i]
                store_idx += 1

        # Move pivot to final position
        nums[store_idx], nums[right] = nums[right], nums[store_idx]

        # Recurse only on the required half
        if store_idx == target_index:
            return nums[store_idx]
        elif store_idx < target_index:
            return quickselect(store_idx + 1, right)
        else:
            return quickselect(left, store_idx - 1)

    return quickselect(0, len(nums) - 1)
```

### QuickSelect Visual Example

Finding 2nd largest in `[3, 2, 1, 5, 6, 4]`:

- 2nd largest = element at index `6 - 2 = 4` (0-indexed) when sorted ascending

```
Initial: [3, 2, 1, 5, 6, 4], target_index = 4

Round 1: pivot = 3
After partition: [2, 1, 3, 5, 6, 4]
                        ^ pivot at index 2
target_index (4) > 2, recurse right: [5, 6, 4]

Round 2: pivot = 5 (from subarray [5, 6, 4] which is indices 3-5)
After partition: [2, 1, 3, 4, 5, 6]
                              ^ pivot at index 4
target_index (4) == 4, return nums[4] = 5 ✓
```

### Approach 3B: Iterative QuickSelect (O(1) Space)

To guarantee $O(1)$ space, we can eliminate the recursion stack entirely.

```python
import random

def find_kth_largest_iterative(nums: list[int], k: int) -> int:
    """
    Iterative QuickSelect.

    Time: O(n) average, O(n²) worst case
    Space: O(1)
    """
    target = len(nums) - k
    left, right = 0, len(nums) - 1

    while left <= right:
        if left == right:
            return nums[left]
            
        pivot_idx = random.randint(left, right)
        pivot = nums[pivot_idx]

        # Move pivot to end
        nums[pivot_idx], nums[right] = nums[right], nums[pivot_idx]

        # Partition
        store = left
        for i in range(left, right):
            if nums[i] < pivot:
                nums[i], nums[store] = nums[store], nums[i]
                store += 1

        # Restore pivot
        nums[store], nums[right] = nums[right], nums[store]

        # Narrow search space
        if store == target:
            return nums[store]
        elif store < target:
            left = store + 1
        else:
            right = store - 1

    return -1 # Should theoretically never be reached
```

---

## Approach 4: Max Heap (Pop K Times)

```python
import heapq

def find_kth_largest_maxheap(nums: list[int], k: int) -> int:
    """
    Build max heap of all elements, pop k times.

    Time: O(n + k log n)
    Space: O(n) for heap
    """
    # Negate for max heap
    max_heap = [-x for x in nums]
    
    # Heapify takes O(n) time
    heapq.heapify(max_heap)

    # Pop k-1 times. Each pop takes O(log n) time
    for _ in range(k - 1):
        heapq.heappop(max_heap)

    return -max_heap[0]
```

This is less efficient than the Min Heap approach when $k \ll n$, but it can be faster if $k$ is extremely small (like $k=1$ or $2$). The space complexity is worse: $O(n)$ instead of $O(k)$.

---

## Using Python's Built-ins

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

Clean and readable. `heapq.nlargest` internally uses an equivalent to the Min Heap approach when $k$ is small, or sorts when $k$ is large.

---

## Comparison of Approaches

| Approach               | Time (Average) | Time (Worst)   | Space     | Best When                      |
| ---------------------- | -------------- | -------------- | --------- | ------------------------------ |
| Sort                   | $O(n \log n)$  | $O(n \log n)$  | $O(1)$*   | $k \approx n$                  |
| Min Heap of size $k$   | $O(n \log k)$  | $O(n \log k)$  | $O(k)$    | $k \ll n$, streaming data      |
| Max Heap of size $n$   | $O(n + k \log n)$ | $O(n + k \log n)$ | $O(n)$ | $k$ is extremely small         |
| QuickSelect            | $O(n)$         | $O(n^2)$       | $O(1)$**  | Fast single query, general use |

\* $O(n)$ if sorting out-of-place (e.g. `sorted()`)
\** Recursive is $O(\log n)$ call stack average, Iterative is strict $O(1)$

**Recommendation:**

- **Interview**: Start with the Min Heap $O(n \log k)$, then implement QuickSelect $O(n)$ average.
- **Production**: `heapq.nlargest()` handles the heavy lifting gracefully.

---

## Variation: Kth Smallest

Same problem, just use different index or heap type:

```python
import heapq

def find_kth_smallest(nums: list[int], k: int) -> int:
    """Find kth smallest element using max heap of size k."""
    # Max heap of size k (negate elements)
    heap = [-x for x in nums[:k]]
    heapq.heapify(heap)
    
    for num in nums[k:]:
        if num < -heap[0]:
            heapq.heapreplace(heap, -num)
            
    return -heap[0]

    # Or simply:
    # return heapq.nsmallest(k, nums)[-1]
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

1. **Start with heap**: $O(n \log k)$, easy to implement correctly.
2. **Mention QuickSelect**: Show you know $O(n)$ is possible.
3. **Discuss trade-offs**: QuickSelect modifies array, has $O(n^2)$ worst case.
4. **Random pivot**: Essential for QuickSelect to avoid worst case on sorted arrays.
5. **Clarify kth**: Is it 0-indexed or 1-indexed? Largest or smallest?

---

## Common Follow-up Questions

**Q: Can you do better than $O(n \log k)$?**
A: Yes, QuickSelect is $O(n)$ average. (And median-of-medians is $O(n)$ worst case).

**Q: What if the array is continuously streaming?**
A: The Min Heap of size $K$ is best because we process one element at a time and maintain a fixed memory footprint of $O(K)$.

**Q: What if $k$ changes frequently?**
A: Maintain a sorted structure (like a balanced BST) or recalculate.

**Q: What if the numbers have a bounded range? (e.g., 0 to 10000)**
A: We can use Counting Sort / Bucket Sort in $O(n)$ time and $O(\text{range})$ space.

---

## Practice Problems

| #   | Problem                                 | Difficulty | Key Variation     |
| --- | --------------------------------------- | ---------- | ----------------- |
| 1   | Kth Largest Element in an Array         | Medium     | Core problem      |
| 2   | Kth Smallest Element in a Sorted Matrix | Medium     | Matrix variation  |
| 3   | Find K Pairs with Smallest Sums         | Medium     | Two arrays        |
| 4   | Kth Smallest Element in a BST           | Medium     | Tree variation    |
| 5   | Third Maximum Number                    | Easy       | Handle duplicates |

---

## Key Takeaways

1. **Heap $O(n \log k)$**: Min heap of size $k$, root is the answer.
2. **QuickSelect $O(n)$**: Partition-based, like QuickSort but only exploring one side.
3. **Random pivot**: Critical for QuickSelect performance.
4. **$k$-th largest = $(n-k)$-th smallest**: Index conversion trick (`len(nums) - k`).
5. **Interview strategy**: Explain Heap first, then QuickSelect.

---

## Next: [05-merge-k-sorted.md](./05-merge-k-sorted.md)

Learn to merge K sorted lists/arrays using heaps.
