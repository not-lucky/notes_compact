# Peak Element

> **Prerequisites:** [Binary Search Template](./01-binary-search-template.md)

## Interview Context

Peak finding demonstrates binary search on non-sorted arrays:
1. **Creative application**: Binary search without sorted order
2. **Neighbor comparison**: Different from typical value comparison
3. **Multiple valid answers**: Any peak is acceptable
4. **Foundation for harder problems**: Bitonic search, local maxima

---

## What is a Peak Element?

A peak element is greater than its neighbors:

```
Array: [1, 3, 5, 4, 2]
            ↑
         Peak at index 2 (value 5)

Boundary rules:
- nums[-1] = nums[n] = -∞
- So first/last element can be peaks if greater than their one neighbor
```

---

## Why Binary Search Works

The key insight: **we can always find a peak by following the uphill direction**.

```
[1, 3, 5, 4, 2]
       M

If nums[mid] < nums[mid+1]:
  There's definitely a peak on the right (or mid+1 is the peak)

If nums[mid] >= nums[mid+1]:
  There's definitely a peak on the left (or mid is the peak)
```

Since boundaries are -∞, moving uphill always leads to a peak.

---

## Find Peak Element

LeetCode 162: Find Peak Element

```python
def find_peak_element(nums: list[int]) -> int:
    """
    Find any peak element in the array.

    Time: O(log n)
    Space: O(1)
    """
    left, right = 0, len(nums) - 1

    while left < right:
        mid = left + (right - left) // 2

        if nums[mid] < nums[mid + 1]:
            # Peak is on the right side
            left = mid + 1
        else:
            # Peak is on the left side (including mid)
            right = mid

    return left
```

---

## Visual Walkthrough

Finding peak in [1, 2, 1, 3, 5, 6, 4]:

```
Step 1: [1, 2, 1, 3, 5, 6, 4]
         L        M        R

         nums[M]=3 < nums[M+1]=5
         Peak on right, L = mid + 1 = 4

Step 2: [1, 2, 1, 3, 5, 6, 4]
                     L  M  R

         nums[M]=6 > nums[M+1]=4
         Peak on left (including mid), R = mid = 5

Step 3: [1, 2, 1, 3, 5, 6, 4]
                     L  R
                     M

         nums[M]=5 < nums[M+1]=6
         L = mid + 1 = 5

Step 4: [1, 2, 1, 3, 5, 6, 4]
                        LR

         L == R, return 5
         nums[5] = 6 is a peak
```

---

## Why This Works: The Proof

1. **Base case**: If array has one element, it's a peak (boundaries are -∞)

2. **Inductive step**:
   - If `nums[mid] < nums[mid+1]`, we move right
   - The subarray `[mid+1, right]` has left boundary `nums[mid]`
   - If `nums[mid+1]` is not the peak, there must be a higher value to its right
   - Eventually we find a peak or reach the boundary (which is -∞)

3. **Similar logic applies when moving left**

---

## Alternative: Recursive Implementation

```python
def find_peak_recursive(nums: list[int], left: int = None, right: int = None) -> int:
    """
    Find peak element recursively.

    Time: O(log n)
    Space: O(log n) - recursion stack
    """
    if left is None:
        left, right = 0, len(nums) - 1

    if left == right:
        return left

    mid = left + (right - left) // 2

    if nums[mid] < nums[mid + 1]:
        return find_peak_recursive(nums, mid + 1, right)
    else:
        return find_peak_recursive(nums, left, mid)
```

---

## Variant: Find All Peaks

```python
def find_all_peaks(nums: list[int]) -> list[int]:
    """
    Find all peak elements in the array.

    Time: O(n) - must check all elements
    Space: O(k) - k peaks
    """
    if not nums:
        return []

    n = len(nums)
    peaks = []

    for i in range(n):
        left_ok = (i == 0) or (nums[i] > nums[i - 1])
        right_ok = (i == n - 1) or (nums[i] > nums[i + 1])

        if left_ok and right_ok:
            peaks.append(i)

    return peaks
```

---

## Peak in Bitonic Array

A bitonic array increases then decreases (exactly one peak):

```python
def find_peak_bitonic(nums: list[int]) -> int:
    """
    Find the peak in a bitonic array.
    Bitonic: strictly increasing then strictly decreasing.

    Time: O(log n)
    Space: O(1)
    """
    left, right = 0, len(nums) - 1

    while left < right:
        mid = left + (right - left) // 2

        if nums[mid] < nums[mid + 1]:
            # Still in increasing part
            left = mid + 1
        else:
            # In decreasing part or at peak
            right = mid

    return left
```

---

## Search in Bitonic Array

First find peak, then binary search both halves:

```python
def search_bitonic(nums: list[int], target: int) -> int:
    """
    Search for target in a bitonic array.

    Time: O(log n)
    Space: O(1)
    """
    # Find peak
    left, right = 0, len(nums) - 1
    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] < nums[mid + 1]:
            left = mid + 1
        else:
            right = mid
    peak = left

    # Search in increasing part (0 to peak)
    result = binary_search_asc(nums, target, 0, peak)
    if result != -1:
        return result

    # Search in decreasing part (peak+1 to end)
    return binary_search_desc(nums, target, peak + 1, len(nums) - 1)


def binary_search_asc(nums, target, left, right):
    """Standard binary search on ascending array."""
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1


def binary_search_desc(nums, target, left, right):
    """Binary search on descending array."""
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] > target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

---

## Peak in 2D Matrix

Find peak in a 2D matrix where you can move in 4 directions:

```python
def find_peak_2d(mat: list[list[int]]) -> list[int]:
    """
    Find peak element in 2D matrix.
    An element is peak if >= all 4 neighbors.

    Time: O(m log n) or O(n log m)
    Space: O(1)
    """
    def get_max_row(col: int) -> int:
        max_row = 0
        for row in range(len(mat)):
            if mat[row][col] > mat[max_row][col]:
                max_row = row
        return max_row

    rows, cols = len(mat), len(mat[0])
    left, right = 0, cols - 1

    while left <= right:
        mid_col = left + (right - left) // 2
        max_row = get_max_row(mid_col)

        # Check if this is a peak
        left_val = mat[max_row][mid_col - 1] if mid_col > 0 else -1
        right_val = mat[max_row][mid_col + 1] if mid_col < cols - 1 else -1

        if mat[max_row][mid_col] >= left_val and mat[max_row][mid_col] >= right_val:
            return [max_row, mid_col]
        elif left_val > mat[max_row][mid_col]:
            right = mid_col - 1
        else:
            left = mid_col + 1

    return [-1, -1]
```

---

## Complexity Analysis

| Problem | Time | Space |
|---------|------|-------|
| Find one peak | O(log n) | O(1) |
| Find all peaks | O(n) | O(k) |
| Peak in bitonic | O(log n) | O(1) |
| Search in bitonic | O(log n) | O(1) |
| Peak in 2D matrix | O(m log n) | O(1) |

---

## Common Mistakes

### 1. Off-by-One in Comparison

```python
# Wrong: comparing with mid-1 instead of mid+1
if nums[mid] < nums[mid - 1]:  # May go out of bounds

# Correct: compare with mid+1 (right neighbor)
if nums[mid] < nums[mid + 1]:
```

### 2. Wrong Loop Condition

```python
# Wrong: using <= causes issues with mid+1 access
while left <= right:
    if nums[mid] < nums[mid + 1]:  # mid+1 might be out of bounds!

# Correct: use < so mid+1 is always valid
while left < right:
```

### 3. Forgetting Boundary Conditions

```python
# Make sure to handle edge cases
# When array has 1 element: return 0
# When array has 2 elements: return index of larger
```

---

## Edge Cases Checklist

- [ ] Single element → return 0
- [ ] Two elements → return index of larger
- [ ] Strictly increasing → return last index
- [ ] Strictly decreasing → return first index
- [ ] All same values → return any index
- [ ] Peak at beginning
- [ ] Peak at end

---

## Practice Problems

| # | Problem | Difficulty | Key Insight |
|---|---------|------------|-------------|
| 1 | Find Peak Element | Medium | Follow uphill direction |
| 2 | Peak Index in Mountain Array | Medium | Same as bitonic peak |
| 3 | Find in Mountain Array | Hard | Find peak + two binary searches |
| 4 | Find a Peak Element II | Medium | Column binary search + row max |
| 5 | Longest Mountain in Array | Medium | Expand from each peak |

---

## Interview Tips

1. **Explain the insight**: Why binary search works on unsorted array
2. **Multiple valid answers**: Clarify any peak is acceptable
3. **Handle boundaries**: First/last elements can be peaks
4. **Prove correctness**: Show uphill always leads to peak
5. **Consider variations**: 2D peaks, all peaks, bitonic

---

## Key Takeaways

1. **Binary search on non-sorted arrays**: Works with monotonic property
2. **Follow uphill direction**: Always leads to a peak
3. **Boundaries are -∞**: Makes first/last elements potential peaks
4. **Bitonic is special case**: Exactly one peak
5. **2D extension exists**: Use column-wise binary search

---

## Next: [06-search-space.md](./06-search-space.md)

Binary search on the answer space for optimization problems.
