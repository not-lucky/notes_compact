def binary_search_rotated(nums: list[int], target: int) -> int:
    """
    Search in a rotated sorted array.
    Pattern: Modified Binary Search
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

    return -1

if __name__ == "__main__":
    # Test cases
    assert binary_search_rotated([4, 5, 6, 7, 0, 1, 2], 0) == 4
    assert binary_search_rotated([4, 5, 6, 7, 0, 1, 2], 3) == -1
    assert binary_search_rotated([1], 0) == -1
    print("All tests passed!")
