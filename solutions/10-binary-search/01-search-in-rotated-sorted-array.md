# Search in Rotated Sorted Array

## Problem Statement

A sorted array is rotated at some pivot unknown to you beforehand (e.g., `[0,1,2,4,5,6,7]` becomes `[4,5,6,7,0,1,2]`).

Given the rotated array and a target value, return the index if found, or -1 if not.

All values are unique.

**Example:**
```
Input: nums = [4, 5, 6, 7, 0, 1, 2], target = 0
Output: 4

Input: nums = [4, 5, 6, 7, 0, 1, 2], target = 3
Output: -1
```

## Approach

### Key Insight
At any point, at least one half of the array is sorted. We can determine which half is sorted and whether the target is in that half.

### Algorithm
1. Find mid element
2. Determine which half is sorted (compare with left)
3. Check if target is in the sorted half
4. Search in the appropriate half

## Implementation

```python
def search(nums: list[int], target: int) -> int:
    """
    Binary search in rotated sorted array.

    Time: O(log n)
    Space: O(1)
    """
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = (left + right) // 2

        if nums[mid] == target:
            return mid

        # Left half is sorted
        if nums[left] <= nums[mid]:
            # Target in left half?
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        # Right half is sorted
        else:
            # Target in right half?
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1

    return -1


def search_with_pivot(nums: list[int], target: int) -> int:
    """
    Alternative: Find pivot first, then binary search.

    Time: O(log n)
    Space: O(1)
    """
    def find_pivot(nums):
        """Find index of minimum element (pivot point)."""
        left, right = 0, len(nums) - 1
        while left < right:
            mid = (left + right) // 2
            if nums[mid] > nums[right]:
                left = mid + 1
            else:
                right = mid
        return left

    def binary_search(left, right):
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return -1

    n = len(nums)
    pivot = find_pivot(nums)

    # Determine which half to search
    if nums[pivot] <= target <= nums[n - 1]:
        return binary_search(pivot, n - 1)
    else:
        return binary_search(0, pivot - 1)
```

## Complexity Analysis

| Aspect | Complexity | Explanation |
|--------|------------|-------------|
| Time | O(log n) | Binary search halves each iteration |
| Space | O(1) | Only pointer variables |

## Visual Walkthrough

```
nums = [4, 5, 6, 7, 0, 1, 2], target = 0

Visualization:
        7
      6
    5
  4           2
            1
          0
  L       M       R

Step 1: left=0, right=6, mid=3
        nums[mid]=7, target=0
        Left sorted (4 <= 7): ✓
        Target in [4,7)? No
        → Search right: left=4

Step 2: left=4, right=6, mid=5
        nums[mid]=1, target=0
        Left sorted (0 <= 1): ✓
        Target in [0,1)? Yes
        → Search left: right=4

Step 3: left=4, right=4, mid=4
        nums[mid]=0 == target
        → Return 4
```

## Edge Cases

1. **Array not rotated**: Works as normal binary search
2. **Single element**: Check if it equals target
3. **Two elements**: Handles correctly
4. **Target at boundaries**: First or last element
5. **Pivot at different positions**: Algorithm handles all cases

## Common Mistakes

1. **Wrong comparison for sorted half**: Use `<=` not `<`
2. **Boundary conditions**: `nums[left] <= target < nums[mid]`
3. **Infinite loop**: Ensure left and right update correctly
4. **Forgetting to check mid**: Check `nums[mid] == target` first

## Variations

### Search in Rotated Array with Duplicates
```python
def search_with_duplicates(nums: list[int], target: int) -> bool:
    """
    Duplicates allowed. Return true/false.

    Time: O(n) worst case (all same elements)
    Space: O(1)
    """
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = (left + right) // 2

        if nums[mid] == target:
            return True

        # Handle duplicates: can't determine sorted half
        if nums[left] == nums[mid] == nums[right]:
            left += 1
            right -= 1
        # Left half is sorted
        elif nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        # Right half is sorted
        else:
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1

    return False
```

### Find Minimum in Rotated Array
```python
def find_min(nums: list[int]) -> int:
    """
    Find minimum element in rotated sorted array.

    Time: O(log n)
    Space: O(1)
    """
    left, right = 0, len(nums) - 1

    while left < right:
        mid = (left + right) // 2

        if nums[mid] > nums[right]:
            # Minimum is in right half
            left = mid + 1
        else:
            # Minimum is in left half (including mid)
            right = mid

    return nums[left]


def find_min_with_duplicates(nums: list[int]) -> int:
    """
    Duplicates allowed.

    Time: O(n) worst case
    Space: O(1)
    """
    left, right = 0, len(nums) - 1

    while left < right:
        mid = (left + right) // 2

        if nums[mid] > nums[right]:
            left = mid + 1
        elif nums[mid] < nums[right]:
            right = mid
        else:
            # nums[mid] == nums[right], can't determine
            right -= 1

    return nums[left]
```

### Find Rotation Count
```python
def find_rotation_count(nums: list[int]) -> int:
    """
    Find how many times array was rotated.
    This equals the index of minimum element.

    Time: O(log n)
    Space: O(1)
    """
    left, right = 0, len(nums) - 1

    # Array not rotated
    if nums[left] <= nums[right]:
        return 0

    while left < right:
        mid = (left + right) // 2

        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid

    return left
```

## Key Pattern: Determining Sorted Half

```python
# If nums[left] <= nums[mid]: left half is sorted
# Otherwise: right half is sorted

# This works because:
# - In a rotated array, exactly one half is always sorted
# - The pivot (minimum) is in the unsorted half
```

## Related Problems

- **Search in Rotated Array II** - With duplicates
- **Find Minimum in Rotated Sorted Array** - Find pivot point
- **Find Minimum in Rotated Sorted Array II** - With duplicates
- **Rotation Count** - Index of minimum element
- **Peak Element** - Similar binary search pattern
