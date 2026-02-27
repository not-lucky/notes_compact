# Lessons

### Binary Search Template Improvements
- Right boundary `find_right_boundary` using `left < len(nums)` check before return is redundant if we initialize `left = 0, right = len(nums) - 1` and never exceed the initial `len(nums) - 1`. The loop `while left < right` guarantees `left` stays within bounds `[0, len(nums) - 1]` assuming `len(nums) > 0` which is handled by early return.
- Explaining Python integer precision is a nice touch to add next to integer overflow guards (`mid = left + (right - left) // 2`).
- `bisect.bisect` is just an alias for `bisect_right`. Make sure to emphasize this since it's commonly asked or used.
- Binary search on answer templates require thinking carefully about whether we want the *first* True or *last* True (usually Left Boundary or Right Boundary template respectively).

### Rotated Sorted Array Details
When breaking the array into 2 passes to do search in rotated sorted array:
1. Target is in right portion if: `target >= nums[0]`? No, that means it's in the left portion!
Actually:
The right sorted portion starts at the pivot. The left portion starts at index 0.
Everything in left portion is `> nums[-1]` and `>= nums[0]`.
Everything in right portion is `<= nums[-1]` and `< nums[0]`.

Wait, let's trace `pivot = min element`.
Array: `[4, 5, 6, 7, 0, 1, 2]`
`pivot` is index `4` (value `0`).
`nums[0]` is `4`. `nums[-1]` is `2`.
If `target == 1`:
`target >= nums[0]` -> `1 >= 4` False.
So it's in right portion.
If `target == 5`:
`target >= nums[0]` -> `5 >= 4` True.
So it's in left portion.

My fix:
```python
    elif target >= nums[0]:
        # Target is in the left sorted subarray
        left, right = 0, pivot - 1
    else:
        # Target is in the right sorted subarray
        left, right = pivot, n - 1
```
This fix is totally correct! I just need to record it in `todo.md` as done.