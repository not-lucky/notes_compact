# Median of Two Sorted Arrays

> **Prerequisites:** [Binary Search Template](./01-binary-search-template.md), [First/Last Occurrence](./02-first-last-occurrence.md)

## Interview Context

This is arguably the most famous "Hard" problem in technical interviews. It's a FANG+ favorite because it tests:

1. **Non-obvious binary search**: Applying binary search not to find a value, but to find a *partitioning index*.
2. **Deep analytical thinking**: Memorization will fail here; you must thoroughly understand the invariants.
3. **Edge case mastery**: Handling out-of-bounds indices, empty arrays, and even/odd total lengths seamlessly.
4. **Optimal complexity**: Finding an $O(\log(\min(m,n)))$ solution when $O(m+n)$ is the obvious baseline.

---

## Building Intuition

### What Is the Median Really?

Before thinking about arrays, let's define the median. The median is the value that **partitions a dataset into two equal halves**, such that every element in the left half is less than or equal to every element in the right half.

```text
Merged: [1, 2, 3, 4, | 5, 6, 7, 8]
                     ↑
             Left Half: [1,2,3,4] (max = 4)
             Right Half: [5,6,7,8] (min = 5)

             Valid because: max(Left) <= min(Right)
             Median = (4+5)/2 = 4.5
```

### The Key Insight: Partition, Don't Merge

The naive approach merges both arrays first ($O(m+n)$), then finds the middle element. But we don't need to *actually* merge the arrays. We just need to find the correct **partition point** across both arrays simultaneously.

```text
nums1: [1, 3, | 8, 9]      partition i=2 (2 elements on left)
nums2: [2, 4, 5, | 7, 10]  partition j=3 (3 elements on left)
                           total left = 5 elements

Combined left half:  [1, 2, 3, 4, 5]
Combined right half: [7, 8, 9, 10]

If max(left) ≤ min(right), this is a valid partition!
```

### Why Binary Search Works Here

We're searching for the correct partition point in `nums1`. Because the total number of elements in the left half is fixed, choosing a partition index in `nums1` strictly dictates the partition index in `nums2`.

```text
Total elements: m + n
Left half must contain: (m + n + 1) // 2 elements

If we take i elements from nums1:
- We MUST take j = (m + n + 1) // 2 - i elements from nums2

So there's only ONE independent variable to search: i.
Since the arrays are sorted, we can binary search for i!
```

### The Valid Partition Condition

A partition is valid if the combined left half is $\le$ the combined right half. Since `nums1` and `nums2` are individually sorted, we already know `nums1[left] <= nums1[right]` and `nums2[left] <= nums2[right]`.

We only need to check the **cross-array elements**:

```text
nums1: [..., A, | B, ...]
nums2: [..., C, | D, ...]

Valid if: A ≤ D  AND  C ≤ B

A is nums1_left  (max of nums1's left side)
C is nums2_left  (max of nums2's left side)
B is nums1_right (min of nums1's right side)
D is nums2_right (min of nums2's right side)
```

### Why Search on the Smaller Array?

We must binary search on the shorter array to ensure $j$ (the partition index in `nums2`) doesn't go negative or out of bounds.

```text
nums1: [1,2,3,4,5,6,7,8,9,10]  (m=10)
nums2: [5]                     (n=1)
Total = 11, left half needs 6 elements

If we search nums1 and guess i=8, then j = 6 - 8 = -2 ← Invalid index!
By searching the smaller array, j is guaranteed to be within [0, n].
```

---

## The Problem

Given two sorted arrays `nums1` and `nums2` of size `m` and `n` respectively, return the median of the two sorted arrays.

**Requirement**: The overall run time complexity should be $O(\log(m+n))$.
*(Note: Searching the smaller array actually gives $O(\log(\min(m,n)))$, which is strictly better and expected in FANG interviews).*

---

## 1. Optimal Solution: Binary Search on Partition

This is the standard expected solution for the hard problem.

### Algorithm
1. Ensure `nums1` is the smaller array.
2. Define `left = 0` and `right = m`.
3. Binary search for `i` (partition in `nums1`), calculate `j` (partition in `nums2`).
4. Handle edge cases using $-\infty$ and $+\infty$ when partitions fall at the very edges of the arrays.
5. Check if the cross-conditions are met:
   - If `nums1_left > nums2_right`: `i` is too far right, move `right = i - 1`.
   - If `nums2_left > nums1_right`: `i` is too far left, move `left = i + 1`.
   - Otherwise, we found the perfect partition! Calculate median based on even/odd total length.

```python
def findMedianSortedArrays(nums1: list[int], nums2: list[int]) -> float:
    # Ensure nums1 is the smaller array to guarantee valid j indices and optimize time
    if len(nums1) > len(nums2):
        return findMedianSortedArrays(nums2, nums1)

    m, n = len(nums1), len(nums2)
    left, right = 0, m
    # (m + n + 1) // 2 ensures left half always has equal or 1 more element than right half
    half_len = (m + n + 1) // 2

    while left <= right:
        # i is the number of elements from nums1 in the left partition
        i = (left + right) // 2
        # j is the number of elements from nums2 in the left partition
        j = half_len - i

        # Extract the 4 elements immediately surrounding the partition.
        # Use -inf / inf if the partition is at the extreme edges.
        nums1_left = nums1[i - 1] if i > 0 else float('-inf')
        nums1_right = nums1[i] if i < m else float('inf')

        nums2_left = nums2[j - 1] if j > 0 else float('-inf')
        nums2_right = nums2[j] if j < n else float('inf')

        # Check if the partition is perfectly valid
        if nums1_left <= nums2_right and nums2_left <= nums1_right:
            # We found the correct partition!
            max_left = max(nums1_left, nums2_left)

            if (m + n) % 2 == 1:
                # Odd total length: median is the maximum of the left partition
                return float(max_left)

            # Even total length: median is average of max(left) and min(right)
            min_right = min(nums1_right, nums2_right)
            return (max_left + min_right) / 2.0

        if nums1_left > nums2_right:
            # nums1's left side is too large. We need to shrink nums1's contribution.
            right = i - 1
        else:
            # nums2's left side is too large. We need to expand nums1's contribution.
            left = i + 1

    raise ValueError("Input arrays are not sorted or are invalid.")
```

### Complexity Analysis
- **Time Complexity:** $O(\log(\min(m, n)))$ because we only binary search the smaller array.
- **Space Complexity:** $O(1)$ since we only store a few pointer variables.

---

## Visual Walkthrough

Finding median of `[1, 3, 8]` and `[2, 4, 5, 7]`:

```text
m=3, n=4, total=7, half=4
Left half must contain exactly 4 elements.

Step 1: left=0, right=3
        i = (0+3)//2 = 1. Therefore, j = 4 - 1 = 3

        nums1: [1 | 3, 8]
        nums2: [2, 4, 5 | 7]

        nums1_left=1, nums1_right=3
        nums2_left=5, nums2_right=7

        Check: 1 <= 7? Yes.
        Check: 5 <= 3? No! (nums2_left > nums1_right)

        Action: We need a larger right element from nums1, so we must increase i.
        left = i + 1 = 2

Step 2: left=2, right=3
        i = (2+3)//2 = 2. Therefore, j = 4 - 2 = 2

        nums1: [1, 3 | 8]
        nums2: [2, 4 | 5, 7]

        nums1_left=3, nums1_right=8
        nums2_left=4, nums2_right=5

        Check: 3 <= 5? Yes.
        Check: 4 <= 8? Yes!

        Action: Valid partition found!
        Total is odd (7), so median = max(nums1_left, nums2_left)
        median = max(3, 4) = 4.0
```

---

## 2. Alternative: Kth Element Approach

While the partition approach is mathematically beautiful, some candidates prefer finding the $k^{th}$ element of two sorted arrays. This solves a slightly more general problem.

If we can find the $k^{th}$ smallest element in $O(\log k)$ time, we can find the median by querying for $k = \lfloor\frac{m+n}{2}\rfloor$ and $k = \lfloor\frac{m+n}{2}\rfloor + 1$.

```python
def findMedianSortedArrays_Kth(nums1: list[int], nums2: list[int]) -> float:
    total_len = len(nums1) + len(nums2)

    def get_kth(k: int, a_start: int, b_start: int) -> int:
        # Base cases
        if a_start >= len(nums1): return nums2[b_start + k - 1]
        if b_start >= len(nums2): return nums1[a_start + k - 1]
        if k == 1: return min(nums1[a_start], nums2[b_start])

        # We want to compare the (k/2)th element of both arrays to discard half of k
        mid = k // 2

        # Determine the index we want to check in both arrays
        # If the array is too short, we assign infinity so we don't discard from it
        a_idx = a_start + mid - 1
        b_idx = b_start + mid - 1

        a_val = nums1[a_idx] if a_idx < len(nums1) else float('inf')
        b_val = nums2[b_idx] if b_idx < len(nums2) else float('inf')

        # If a_val is smaller, we can safely discard the first mid elements of nums1
        # because the kth smallest element MUST be greater than or equal to a_val.
        if a_val < b_val:
            return get_kth(k - mid, a_start + mid, b_start)
        else:
            return get_kth(k - mid, a_start, b_start + mid)

    # Calculate k for both odd and even cases
    left = get_kth((total_len + 1) // 2, 0, 0)
    if total_len % 2 == 1:
        return float(left)
    else:
        right = get_kth(total_len // 2 + 1, 0, 0)
        return (left + right) / 2.0
```

### Complexity Analysis
- **Time Complexity:** $O(\log(m+n))$ since we discard roughly half of $k$ at each recursive step, and initially $k \approx \frac{m+n}{2}$.
- **Space Complexity:** $O(\log(m+n))$ for the recursion stack (or $O(1)$ if converted to iterative).

---

## Common Interview Pitfalls

1. **Forgetting to Swap for Smaller Array**
   If you don't ensure `nums1` is the smaller array, `j` could become negative during the binary search, causing `IndexError` (or incorrect out of bounds access in languages that support negative indexing like Python).
   ```python
   if len(nums1) > len(nums2):
       return findMedianSortedArrays(nums2, nums1)
   ```

2. **Mishandling Infinity at Boundaries**
   When `i = 0`, it means the left partition contains NO elements from `nums1`. The maximum value of an empty set is $-\infty$, meaning it will safely pass the `nums1_left <= nums2_right` check.
   ```python
   # Correct boundary handling
   nums1_left = nums1[i - 1] if i > 0 else float('-inf')
   ```

3. **Wrong "Half Length" Math**
   Using `(m + n) // 2` causes logic errors for odd-length combinations. Always use `(m + n + 1) // 2` which gracefully handles both even and odd totals without extra conditional branching inside the loop parameters.

---

## Extensions and Related Problems

### 1. Find Kth Smallest in Two Sorted Arrays
Directly solved using the $k^{th}$ element approach above.

### 2. Median of K Sorted Arrays
This requires shifting from a Binary Search approach to a **Min-Heap (Priority Queue)** approach.

```python
import heapq

def median_k_arrays(arrays: list[list[int]]) -> float:
    # Time: O(total * log K) where K is number of arrays
    total_elements = sum(len(arr) for arr in arrays)
    if total_elements == 0:
        return 0.0

    # target is the 1-based index of the middle element
    target = (total_elements + 1) // 2

    heap = []
    # Initialize heap with the first element of each array
    for i, arr in enumerate(arrays):
        if arr:
            heapq.heappush(heap, (arr[0], i, 0))

    count = 0
    prev_val = curr_val = 0

    while heap:
        prev_val = curr_val
        curr_val, arr_idx, elem_idx = heapq.heappop(heap)
        count += 1

        if count == target:
            if total_elements % 2 == 1:
                return float(curr_val)
            # If total_elements is even, we need the NEXT element to average them.
            # We don't return yet, we let the loop run one more time.

        elif count == target + 1 and total_elements % 2 == 0:
            return (prev_val + curr_val) / 2.0

        # Push the next element from the same array into the heap
        if elem_idx + 1 < len(arrays[arr_idx]):
            next_val = arrays[arr_idx][elem_idx + 1]
            heapq.heappush(heap, (next_val, arr_idx, elem_idx + 1))

    return 0.0
```

### 3. Find Median from Data Stream
When the arrays are dynamically growing, the partition binary search fails. You must switch to the **Two Heaps** pattern (a Max-Heap for the left half, and a Min-Heap for the right half) to keep the median balanced in $O(\log n)$ per insertion. *(Covered extensively in the Heaps chapter)*.

---

## Summary of Approaches

| Approach | Time Complexity | Space Complexity | Best When... |
|----------|----------------|-----------------|--------------|
| **Binary Search Partition** | $O(\log(\min(m,n)))$ | $O(1)$ | FANG interviews. Expected optimal solution. |
| **Kth Element (Recursive)** | $O(\log(m+n))$ | $O(\log(m+n))$ | Solving the more generic "find Kth" variant. |
| **Two Pointers Merge** | $O(m+n)$ | $O(1)$ | The interviewer asks for the brute force first. |
| **Min-Heap Merge** | $O((m+n) \log K)$ | $O(K)$ | There are $>2$ sorted arrays to process. |

---

## Final Checklist for Interviews

- [ ] Acknowledge the naive $O(m+n)$ approach immediately to establish a baseline.
- [ ] Diagram the partition concept. Showing the "cut" visually proves you understand the invariant.
- [ ] Emphasize that finding `i` *guarantees* `j` because the left partition size is constant.
- [ ] Dry-run the edge cases (especially $m=0$) before the interviewer points them out.
