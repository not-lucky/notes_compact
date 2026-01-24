def cyclic_sort(nums: list[int]) -> list[int]:
    """
    Sort an array containing values from 1 to n in-place.
    Pattern: Cyclic Sort
    Time: O(n)
    Space: O(1)
    """
    i = 0
    while i < len(nums):
        # The correct index for value x is x - 1
        correct_idx = nums[i] - 1

        if nums[i] != nums[correct_idx]:
            # Swap
            nums[i], nums[correct_idx] = nums[correct_idx], nums[i]
        else:
            i += 1
    return nums

if __name__ == "__main__":
    # Test cases
    assert cyclic_sort([3, 1, 5, 4, 2]) == [1, 2, 3, 4, 5]
    assert cyclic_sort([2, 6, 4, 3, 1, 5]) == [1, 2, 3, 4, 5, 6]
    print("All tests passed!")
