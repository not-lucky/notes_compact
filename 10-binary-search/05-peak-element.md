# Peak Element

> **Prerequisites:** [Binary Search Template](./01-binary-search-template.md)

## Interview Context

Peak finding demonstrates an advanced and creative use of binary search on **non-sorted** arrays. It tests your ability to adapt standard algorithms to non-standard properties.

1. **Creative application**: Binary search on an unsorted array based on local properties rather than global ordering.
2. **Neighbor comparison**: Comparing elements to their adjacent neighbors rather than a fixed target.
3. **Multiple valid answers**: Returning any valid peak is acceptable.
4. **Foundation for harder problems**: Precursor to bitonic search, finding local extrema in 2D matrices, and optimization functions.

---

## Building Intuition

### What Is a Peak?

A peak element is strictly greater than its neighbors:

```text
Array: [1, 3, 5, 4, 2]
            ↑
         5 is a PEAK: 5 > 3 (left) and 5 > 4 (right)
```

**Boundary Rule**: Elements at the edges only need to be strictly greater than their ONE adjacent neighbor. This is logically equivalent to imagining that out-of-bounds elements are negative infinity (`nums[-1] = nums[n] = -∞`).

### Why Does Binary Search Work on Unsorted Data?

This is the non-intuitive part. How can we eliminate half the search space if the array isn't sorted?

The key insight: **We are guaranteed to find AT LEAST ONE peak by simply following the uphill slope.**

```text
[1, 2, 1, 3, 5, 6, 4]
          M

nums[mid] = 3
nums[mid+1] = 5

Since 3 < 5, we go RIGHT. Why?
```

Because if we move to the right (to 5), one of three things must happen:
1. `5` is a peak (if `5 > 6`, which it isn't here, but could be in another array).
2. The sequence continues to go up, eventually hitting a peak.
3. The sequence continues to go up until the end of the array. Since the out-of-bounds value is `-∞`, the very last element would be a peak.

**No matter what, going uphill ALWAYS leads to a peak!**

### Mental Model: Climbing a Mountain

Imagine you're blindfolded on a mountain range. You can only feel the slope directly under your feet.
- If the ground slopes UP to your right → step right (you are guaranteed to find a peak or summit).
- If the ground slopes UP to your left → step left.
- If you're at a local maximum (both sides slope down) → you found a peak!

You might not find the *highest* peak (global maximum), but you will definitively find *a* peak (local maximum).

### The Mathematical Guarantee

Why must following the uphill direction lead to a peak?

1. If `nums[mid] < nums[mid+1]`, we move right.
2. The right portion either:
   - Contains a peak somewhere within it, OR
   - Keeps increasing monotonically until the rightmost boundary.
3. At the rightmost boundary `n-1`, by definition, `nums[n] = -∞`.
4. Therefore, if the sequence only increases, the last element before the boundary `nums[n-1]` IS a peak because `nums[n-1] > nums[n-2]` (it was increasing) and `nums[n-1] > -∞`.

### Multiple Peaks Don't Matter

```text
[1, 3, 1, 5, 1, 7, 1]
    ↑     ↑     ↑
   All three are valid peaks.
```
Binary search finds ONE of them based on the initial `mid` selection and subsequent slope tracking. This is perfectly acceptable for standard peak-finding problems.

---

## When NOT to Use Peak Binary Search

**1. You Need THE Maximum (Global Maximum, Not Just A Peak)**
- Peak search finds *a* local maximum.
- If you need the *global* maximum in an unsorted array, you need an $O(n)$ linear scan.

**2. You Need ALL Peaks**
- Finding all peaks requires checking every element, so an $O(n)$ linear scan is mandatory.

**3. Equal Adjacent Elements Are Allowed (Plateaus)**
- If `nums[i] == nums[i+1]` is possible, the "uphill" direction is ambiguous (a plateau). Binary search cannot definitively choose left or right to guarantee finding a peak.
- Standard $O(\log n)$ peak finding requires *strictly* unequal adjacent elements (or a strict definition of a peak that accounts for plateaus in a way that allows binary search, which is rare).

**4. Very Small Arrays ($n \le 3$)**
- While binary search works, direct comparisons are simpler and faster in practice.

**🚩 Red Flags for Standard Binary Search:**
- "Find the *maximum* element" → $O(n)$ scan.
- "Find *all* peaks" → $O(n)$ scan.
- "Elements may be *equal*" → Binary search might degrade to $O(n)$ or require complex modifications.

---

## Core Implementation: Find Peak Element

**LeetCode 162: Find Peak Element**

```python
def find_peak_element(nums: list[int]) -> int:
    """
    Find any peak element in the array and return its index.
    Assumption: nums[i] != nums[i+1] for all valid i.

    Time: O(log n)
    Space: O(1)
    """
    left, right = 0, len(nums) - 1

    # Standard template for finding an index where a condition is met
    # Notice the condition `left < right`
    while left < right:
        mid = left + (right - left) // 2

        # Compare mid with its right neighbor to determine slope
        if nums[mid] < nums[mid + 1]:
            # The slope is increasing upwards to the right.
            # A peak MUST exist to the right of mid.
            # mid itself cannot be the peak because its right neighbor is larger.
            left = mid + 1
        else:
            # The slope is decreasing downwards to the right (nums[mid] > nums[mid+1]).
            # A peak MUST exist to the left of mid+1.
            # mid ITSELF could be the peak, so we include it in the search space.
            right = mid

    # Loop terminates when left == right.
    # Because our logic guarantees the search space always contains a peak,
    # the single remaining element must be a peak.
    return left
```

### Visual Walkthrough

Finding a peak in `[1, 2, 1, 3, 5, 6, 4]`:

```text
Step 1: [1, 2, 1, 3, 5, 6, 4]
         L        M        R
         nums[M]=3 < nums[M+1]=5
         Slope is up to the right. Peak is strictly to the right.
         left = mid + 1 = 4

Step 2: [1, 2, 1, 3, 5, 6, 4]
                     L  M  R
         nums[M]=6 > nums[M+1]=4
         Slope is down to the right. Peak is at mid or to its left.
         right = mid = 5

Step 3: [1, 2, 1, 3, 5, 6, 4]
                     L  R
                     M
         nums[M]=5 < nums[M+1]=6
         Slope is up to the right. Peak is strictly to the right.
         left = mid + 1 = 5

Step 4: [1, 2, 1, 3, 5, 6, 4]
                        LR
         left == right. Loop terminates.
         Return left (index 5). nums[5] = 6 is indeed a peak.
```

---

## Advanced Variants

### 1. Peak in a Bitonic Array

A bitonic array strictly increases then strictly decreases. It has **exactly one** peak (the global maximum). The standard peak-finding algorithm works perfectly here.

```python
def peak_index_in_mountain_array(arr: list[int]) -> int:
    """
    Find the peak index in a mountain (bitonic) array.
    Guaranteed: arr strictly increases then strictly decreases.

    Time: O(log n)
    Space: O(1)
    """
    left, right = 0, len(arr) - 1

    while left < right:
        mid = left + (right - left) // 2

        if arr[mid] < arr[mid + 1]:
            # We are on the ascending slope
            left = mid + 1
        else:
            # We are on the descending slope, or exactly at the peak
            right = mid

    return left
```

### 2. Search in a Bitonic Array

**LeetCode 1095: Find in Mountain Array**

To search for a target in a bitonic array:
1. Find the peak index (using the logic above).
2. Binary search the strictly ascending left half `[0, peak]`.
3. If not found, binary search the strictly descending right half `[peak + 1, n - 1]`.

```python
class Solution:
    def findInMountainArray(self, target: int, mountain_arr: 'MountainArray') -> int:
        n = mountain_arr.length()

        # 1. Find the peak
        left, right = 0, n - 1
        while left < right:
            mid = left + (right - left) // 2
            if mountain_arr.get(mid) < mountain_arr.get(mid + 1):
                left = mid + 1
            else:
                right = mid
        peak = left

        # 2. Binary search ascending left half
        def search_asc(left, right):
            while left <= right:
                mid = left + (right - left) // 2
                val = mountain_arr.get(mid)
                if val == target:
                    return mid
                elif val < target:
                    left = mid + 1
                else:
                    right = mid - 1
            return -1

        res = search_asc(0, peak)
        if res != -1:
            return res

        # 3. Binary search descending right half
        def search_desc(left, right):
            while left <= right:
                mid = left + (right - left) // 2
                val = mountain_arr.get(mid)
                if val == target:
                    return mid
                elif val > target: # Note the flipped comparison for descending
                    left = mid + 1
                else:
                    right = mid - 1
            return -1

        return search_desc(peak + 1, n - 1)
```

### 3. Peak in a 2D Matrix

**LeetCode 1901: Find a Peak Element II**

Find a peak in an $m \times n$ matrix where an element is strictly greater than its adjacent (top, bottom, left, right) neighbors. No two adjacent cells are equal.

**Insight:** Apply binary search on the *columns*.
1. Pick middle column `mid_col`.
2. Find the global maximum element in this column at `row = max_row`.
3. Compare `mat[max_row][mid_col]` with its left and right neighbors `mat[max_row][mid_col-1]` and `mat[max_row][mid_col+1]`.
4. Because we chose the maximum element in the column, it is guaranteed to be greater than its top and bottom neighbors. We only need to resolve the left/right condition.
5. If the left neighbor is greater, search the left half of columns. Otherwise, search the right half.

```python
def findPeakGrid(mat: list[list[int]]) -> list[int]:
    """
    Find any peak element in a 2D matrix.

    Time: O(m * log n) where m is rows, n is cols.
    Space: O(1)
    """
    rows, cols = len(mat), len(mat[0])
    left_col, right_col = 0, cols - 1

    while left_col <= right_col:
        mid_col = left_col + (right_col - left_col) // 2

        # Find the row index of the maximum element in the current column
        max_row = 0
        for r in range(rows):
            if mat[r][mid_col] > mat[max_row][mid_col]:
                max_row = r

        # Compare with left and right neighbors
        left_val = mat[max_row][mid_col - 1] if mid_col > 0 else -1
        right_val = mat[max_row][mid_col + 1] if mid_col < cols - 1 else -1

        current_val = mat[max_row][mid_col]

        if current_val > left_val and current_val > right_val:
            return [max_row, mid_col]
        elif left_val > current_val:
            # Peak must be in the left columns
            right_col = mid_col - 1
        else:
            # Peak must be in the right columns
            left_col = mid_col + 1

    return [-1, -1] # Unreachable if array follows constraints
```

---

## Complexity Analysis

| Problem | Approach | Time Complexity | Space Complexity |
| :--- | :--- | :--- | :--- |
| **Find One Peak (1D)** | Binary Search | $O(\log n)$ | $O(1)$ |
| **Find All Peaks (1D)** | Linear Scan | $O(n)$ | $O(k)$ for $k$ peaks |
| **Search in Bitonic Array**| 3 Binary Searches | $O(\log n)$ | $O(1)$ |
| **Find Peak Element II (2D)** | Binary Search on Columns | $O(m \log n)$ | $O(1)$ |

---

## Common Mistakes

### 1. Wrong Loop Condition & Out-of-Bounds Error

**The Error:** Using `while left <= right:` and then checking `nums[mid] < nums[mid+1]`. If `left == right`, `mid` is the last element, and `mid + 1` causes an IndexError.
**The Fix:** Use `while left < right:` when checking `mid + 1`. This guarantees `mid` can never be the last index of the search space.

```python
# WRONG
while left <= right:
    # Danger: if mid == len(nums)-1, nums[mid+1] throws IndexError
    if nums[mid] < nums[mid+1]: ...

# CORRECT
while left < right:
    # Safe: left < right implies right >= left + 1, so mid <= right - 1.
    # Therefore mid + 1 <= right, preventing out-of-bounds access.
    if nums[mid] < nums[mid+1]: ...
```

### 2. Incorrect State Update

**The Error:** `left = mid` or `right = mid - 1`.
**The Fix:** If `nums[mid] < nums[mid+1]`, `mid` CANNOT be the peak (its right neighbor is larger). We can safely eliminate `mid` and set `left = mid + 1`. If `nums[mid] > nums[mid+1]`, `mid` COULD be the peak, so we must retain it in the search space with `right = mid`.

---

## Edge Cases to Consider

- **Array of length 1:** Handled perfectly by `while left < right` (loop never runs, returns `left = 0`).
- **Array of length 2:** e.g., `[2, 1]` or `[1, 2]`. Correctly steps left or right and returns the max.
- **Strictly Increasing (`[1, 2, 3, 4, 5]`):** Always updates `left = mid + 1`, eventually returning the last index.
- **Strictly Decreasing (`[5, 4, 3, 2, 1]`):** Always updates `right = mid`, eventually returning the first index `0`.

---

## Practice Problems

| Problem | Difficulty | Key Insight |
| :--- | :---: | :--- |
| [162. Find Peak Element](https://leetcode.com/problems/find-peak-element/) | Medium | Standard application of following the uphill slope. |
| [852. Peak Index in a Mountain Array](https://leetcode.com/problems/peak-index-in-a-mountain-array/) | Medium | Identical to 162, but guarantees only a single peak exists. |
| [1095. Find in Mountain Array](https://leetcode.com/problems/find-in-mountain-array/) | Hard | Find peak first, then binary search ascending/descending halves. |
| [1901. Find a Peak Element II](https://leetcode.com/problems/find-a-peak-element-ii/) | Medium | Binary search on columns. Find max in mid col, check L/R neighbors. |

---

## Next: [06-search-space.md](./06-search-space.md)

Explore **Binary Search on Answer Space**, a crucial pattern for optimization problems where you search for a target value rather than an array index.