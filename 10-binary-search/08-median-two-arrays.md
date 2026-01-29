# Median of Two Sorted Arrays

> **Prerequisites:** [Binary Search Template](./01-binary-search-template.md), [First/Last Occurrence](./02-first-last-occurrence.md)

## Interview Context

This is a classic hard problem and FANG+ favorite because:

1. **Non-obvious binary search**: Requires creative application
2. **Edge case heavy**: Many boundary conditions
3. **Optimal solution is tricky**: O(log(min(m,n))) is not intuitive
4. **Tests deep understanding**: Not pattern matching

---

## Building Intuition

**What Is the Median Really?**

The median is the value that PARTITIONS the data into two equal halves:

```
Merged: [1, 2, 3, 4, 5, 6, 7, 8]
                  ↑
             Left Half: [1,2,3,4]
             Right Half: [5,6,7,8]
             Median = (4+5)/2 = 4.5
```

**The Key Insight: Partition, Don't Merge**

The naive approach merges both arrays first (O(m+n)), then finds the middle.

But here's the insight: we don't need to ACTUALLY merge. We just need to find the correct PARTITION POINT.

```
nums1: [1, 3, | 8, 9]      partition i=2 (2 elements on left)
nums2: [2, 4, 5, | 7, 10]  partition j=3 (3 elements on left)
                           total left = 5 elements

Combined left half:  [1, 2, 3, 4, 5]
Combined right half: [7, 8, 9, 10]

If max(left) ≤ min(right), this is a valid partition!
```

**Why Binary Search Works Here**

We're searching for the correct partition point in nums1. Given how many elements we take from nums1, we can calculate how many to take from nums2.

```
Total elements: m + n
Left half should have: (m + n + 1) // 2 elements

If we take i elements from nums1:
- We must take j = (m+n+1)//2 - i elements from nums2

So there's only ONE variable to search: i
Binary search on i!
```

**The Valid Partition Condition**

A partition is valid if left half ≤ right half. Since both arrays are sorted internally, we only need to check the CROSS elements:

```
nums1: [..., A, | B, ...]
nums2: [..., C, | D, ...]

Valid if: A ≤ D  AND  C ≤ B

A is max of nums1's left side
C is max of nums2's left side
B is min of nums1's right side
D is min of nums2's right side
```

**Mental Model: Cutting Two Ropes**

Imagine two ropes (sorted arrays) that you want to combine into one sorted rope. You need to cut each rope at some point, then verify that the left pieces fit before the right pieces.

- Cut rope1 at position i, rope2 at position j
- The last bead on rope1's left piece must be smaller than rope2's first right bead
- The last bead on rope2's left piece must be smaller than rope1's first right bead

**Why Search on the Smaller Array?**

If we search on the larger array, the partition j might go negative:

```
nums1: [1,2,3,4,5,6,7,8,9,10]  (m=10)
nums2: [5]                      (n=1)
Total = 11, left half needs 6 elements

If i=8 (from nums1), j = 6-8 = -2 ← Invalid!
```

By searching on the smaller array, j always stays valid.

**Visual Walkthrough**

```
nums1: [1, 3, 8]  (m=3)
nums2: [2, 4, 5, 7]  (n=4)
Total = 7, left half needs 4 elements

Step 1: Binary search on nums1 (0 to 3)
  i = 1, j = 4-1 = 3
  nums1: [1 | 3, 8]
  nums2: [2, 4, 5 | 7]

  Check: nums1[0]=1 ≤ nums2[3]=7 ✓
         nums2[2]=5 ≤ nums1[1]=3 ✗

  nums2's left max (5) > nums1's right min (3)
  Need MORE from nums1! left = i+1 = 2

Step 2:
  i = 2, j = 4-2 = 2
  nums1: [1, 3 | 8]
  nums2: [2, 4 | 5, 7]

  Check: nums1[1]=3 ≤ nums2[2]=5 ✓
         nums2[1]=4 ≤ nums1[2]=8 ✓

  Valid partition!
  Odd total: median = max(3, 4) = 4
```

---

## When NOT to Use This Approach

**1. Arrays Aren't Sorted**

This entire approach relies on sorted order. Unsorted arrays need:

- Sort first: O(n log n + m log m)
- Or use quickselect: O(n + m) average

**2. Finding Other Quantiles**

This partition approach is specific to median. For:

- 25th percentile → Modify partition sizes
- kth element → Use the kth element approach (also provided below)

**3. More Than Two Arrays**

For k sorted arrays, use:

- Heap-based merge: O(total × log k)
- Not a simple generalization of this approach

**4. Very Small Arrays**

If m + n ≤ 10:

- Just merge and find middle: O(m + n)
- Simpler to implement, same practical speed

**5. Streaming Data**

If arrays are being appended to:

- Two-heap approach is better
- This approach needs complete arrays

**Red Flags:**

- "Arrays may be unsorted" → Sort first or different approach
- "Multiple arrays" → Heap-based merge
- "Running median as elements arrive" → Two-heap approach
- "Very large arrays that don't fit in memory" → External merge sort

---

## The Problem

Given two sorted arrays `nums1` and `nums2`, find the median of the combined sorted array.

```
nums1 = [1, 3]
nums2 = [2]
Merged = [1, 2, 3]
Median = 2.0

nums1 = [1, 2]
nums2 = [3, 4]
Merged = [1, 2, 3, 4]
Median = (2 + 3) / 2 = 2.5
```

**Requirement**: O(log(m+n)) time complexity.

---

## Binary Search on Partition

```python
def find_median_sorted_arrays(nums1: list[int], nums2: list[int]) -> float:
    """
    Find median of two sorted arrays.

    Time: O(log(min(m, n)))
    Space: O(1)
    """
    # Ensure nums1 is the smaller array
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1

    m, n = len(nums1), len(nums2)
    total = m + n
    half = (total + 1) // 2

    left, right = 0, m

    while left <= right:
        # Partition positions
        i = (left + right) // 2  # Elements from nums1 in left half
        j = half - i              # Elements from nums2 in left half

        # Edge values (use -inf/inf for boundaries)
        nums1_left = nums1[i - 1] if i > 0 else float('-inf')
        nums1_right = nums1[i] if i < m else float('inf')
        nums2_left = nums2[j - 1] if j > 0 else float('-inf')
        nums2_right = nums2[j] if j < n else float('inf')

        # Check if partition is valid
        if nums1_left <= nums2_right and nums2_left <= nums1_right:
            # Valid partition found
            if total % 2 == 1:
                # Odd total: median is max of left half
                return max(nums1_left, nums2_left)
            else:
                # Even total: average of max(left) and min(right)
                return (max(nums1_left, nums2_left) +
                        min(nums1_right, nums2_right)) / 2

        elif nums1_left > nums2_right:
            # nums1 partition too far right
            right = i - 1
        else:
            # nums1 partition too far left
            left = i + 1

    raise ValueError("Arrays are not sorted")
```

---

## Visual Walkthrough

Finding median of [1, 3, 8] and [2, 4, 5, 7]:

```
m=3, n=4, total=7, half=4

Step 1: left=0, right=3
        i=1, j=3
        nums1: [1 | 3, 8]
        nums2: [2, 4, 5 | 7]

        nums1_left=1, nums1_right=3
        nums2_left=5, nums2_right=7

        Check: 1 <= 7? Yes. 5 <= 3? No!
        nums2_left > nums1_right: need more from nums1
        left = i + 1 = 2

Step 2: left=2, right=3
        i=2, j=2
        nums1: [1, 3 | 8]
        nums2: [2, 4 | 5, 7]

        nums1_left=3, nums1_right=8
        nums2_left=4, nums2_right=5

        Check: 3 <= 5? Yes. 4 <= 8? Yes!
        Valid partition!

        Odd total: return max(3, 4) = 4
```

---

## Why Binary Search Works

1. **We only search on the smaller array** (nums1)
2. **For each partition i in nums1, j is determined**: j = half - i
3. **Monotonic property**: If current partition is too far right, all further right are also invalid
4. **Binary search finds the correct partition** in O(log m)

---

## Alternative: Kth Element Approach

Find the kth smallest element in two sorted arrays:

```python
def find_kth_element(nums1: list[int], nums2: list[int], k: int) -> int:
    """
    Find kth smallest element in two sorted arrays.

    Time: O(log k)
    Space: O(1)
    """
    m, n = len(nums1), len(nums2)
    i, j = 0, 0  # Starting indices

    while True:
        # Edge cases
        if i >= m:
            return nums2[j + k - 1]
        if j >= n:
            return nums1[i + k - 1]
        if k == 1:
            return min(nums1[i], nums2[j])

        # Compare elements at k//2 positions
        mid = k // 2
        new_i = min(i + mid, m) - 1
        new_j = min(j + mid, n) - 1

        if nums1[new_i] <= nums2[new_j]:
            # Discard left part of nums1
            k -= (new_i - i + 1)
            i = new_i + 1
        else:
            # Discard left part of nums2
            k -= (new_j - j + 1)
            j = new_j + 1


def find_median_via_kth(nums1: list[int], nums2: list[int]) -> float:
    """
    Find median using kth element approach.

    Time: O(log(m + n))
    Space: O(1)
    """
    total = len(nums1) + len(nums2)

    if total % 2 == 1:
        return find_kth_element(nums1, nums2, total // 2 + 1)
    else:
        left = find_kth_element(nums1, nums2, total // 2)
        right = find_kth_element(nums1, nums2, total // 2 + 1)
        return (left + right) / 2
```

---

## Comparison of Approaches

| Approach      | Time            | Space | Complexity  |
| ------------- | --------------- | ----- | ----------- |
| Partition     | O(log min(m,n)) | O(1)  | Medium-High |
| Kth Element   | O(log(m+n))     | O(1)  | Medium      |
| Merge First k | O(k) = O(m+n)   | O(1)  | Low         |

The partition approach is slightly faster but harder to implement correctly.

---

## Edge Cases

### One Array Empty

```python
nums1 = []
nums2 = [1, 2, 3]
# Median is just median of nums2
```

### Arrays of Different Sizes

```python
nums1 = [1, 2]
nums2 = [3, 4, 5, 6, 7, 8]
# Still works with partition approach
```

### Single Elements

```python
nums1 = [1]
nums2 = [2]
# Median = (1 + 2) / 2 = 1.5
```

### Duplicates

```python
nums1 = [1, 1, 1]
nums2 = [1, 1, 1]
# Median = 1
```

---

## Related Problems

### Find Kth Smallest in Two Arrays

```python
def kth_smallest_two_arrays(nums1: list[int], nums2: list[int], k: int) -> int:
    """Direct application of kth element approach."""
    return find_kth_element(nums1, nums2, k)
```

### Median of Multiple Sorted Arrays

For more than 2 arrays, use a min-heap approach:

```python
import heapq

def median_multiple_arrays(arrays: list[list[int]]) -> float:
    """
    Find median of multiple sorted arrays.

    Time: O(total * log k) where k = number of arrays
    Space: O(k)
    """
    total = sum(len(arr) for arr in arrays)
    target = (total + 1) // 2

    # Min heap: (value, array_index, element_index)
    heap = []
    for i, arr in enumerate(arrays):
        if arr:
            heapq.heappush(heap, (arr[0], i, 0))

    count = 0
    prev = curr = 0

    while heap:
        prev = curr
        curr, arr_idx, elem_idx = heapq.heappop(heap)
        count += 1

        if count == target:
            if total % 2 == 1:
                return curr
            # Need one more for even total

        if count == target + 1 and total % 2 == 0:
            return (prev + curr) / 2

        # Add next element from same array
        if elem_idx + 1 < len(arrays[arr_idx]):
            next_val = arrays[arr_idx][elem_idx + 1]
            heapq.heappush(heap, (next_val, arr_idx, elem_idx + 1))

    return curr
```

---

## Common Mistakes

### 1. Not Ensuring nums1 is Smaller

```python
# Wrong: not swapping
# Binary search on larger array may go out of bounds

# Correct
if len(nums1) > len(nums2):
    nums1, nums2 = nums2, nums1
```

### 2. Wrong Boundary Values

```python
# Wrong: using 0 or len(array)
nums1_left = nums1[i - 1] if i > 0 else 0  # Should be -inf

# Correct
nums1_left = nums1[i - 1] if i > 0 else float('-inf')
nums1_right = nums1[i] if i < m else float('inf')
```

### 3. Off-by-One in Half Calculation

```python
# For median, left half should have (total + 1) // 2 elements
half = (total + 1) // 2  # Correct for both odd and even
```

### 4. Wrong Final Answer for Even Total

```python
# Even total: average of two middle elements
if total % 2 == 0:
    return (max(nums1_left, nums2_left) +
            min(nums1_right, nums2_right)) / 2
```

---

## Step-by-Step Implementation Guide

1. **Ensure nums1 is smaller** (reduces search space)
2. **Calculate half** = (m + n + 1) // 2
3. **Binary search on nums1**: from 0 to m
4. **For each i, calculate j** = half - i
5. **Get boundary values** with -inf/inf for edges
6. **Check partition validity**: left maxes ≤ right mins
7. **Adjust search range** based on which condition fails
8. **Return median** based on odd/even total

---

## Complexity Analysis

| Operation            | Time                       | Space    |
| -------------------- | -------------------------- | -------- |
| Partition approach   | O(log min(m,n))            | O(1)     |
| Kth element approach | O(log k) where k = (m+n)/2 | O(1)     |
| Naive merge          | O(m + n)                   | O(m + n) |

---

## Edge Cases Checklist

- [ ] One array empty
- [ ] Both arrays have one element
- [ ] Arrays of very different sizes
- [ ] All elements in one array < all in other
- [ ] Duplicate elements
- [ ] Odd vs even total length

---

## Practice Problems

| #   | Problem                               | Difficulty | Key Insight             |
| --- | ------------------------------------- | ---------- | ----------------------- |
| 1   | Median of Two Sorted Arrays           | Hard       | Partition binary search |
| 2   | Kth Smallest Element in Sorted Matrix | Medium     | Related technique       |
| 3   | Find K Pairs with Smallest Sums       | Medium     | Heap + binary search    |
| 4   | Merge K Sorted Lists                  | Hard       | Heap approach           |
| 5   | Find Median from Data Stream          | Hard       | Two heaps               |

---

## Interview Tips

1. **Start with brute force**: Mention O(m+n) merge approach first
2. **Explain the partition idea**: Draw the arrays with partition
3. **Handle edge cases explicitly**: Empty arrays, boundaries
4. **Test with examples**: Walk through a small case
5. **Mention complexity**: O(log min(m,n)) is optimal

---

## Key Takeaways

1. **Partition-based approach**: Find correct split point
2. **Search on smaller array**: Reduces time complexity
3. **Use -inf/inf for boundaries**: Handles edge cases cleanly
4. **Two conditions for valid partition**: Check both
5. **Different formulas for odd/even**: Know both cases

---

## Summary: Binary Search Patterns

This concludes Chapter 10 on Binary Search. The key patterns covered:

| Pattern               | Key Insight                    |
| --------------------- | ------------------------------ |
| Standard Template     | Find exact match or boundary   |
| First/Last Occurrence | Continue searching after match |
| Rotated Array         | Identify sorted half           |
| Find Minimum          | Compare with right boundary    |
| Peak Element          | Follow uphill direction        |
| Search Space          | Binary search on answer range  |
| Matrix Search         | 1D conversion or staircase     |
| Median Two Arrays     | Partition both arrays          |

Mastering these patterns will prepare you for most binary search problems in FANG+ interviews.
