# Lessons

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
