def two_sum_sorted(nums: list[int], target: int) -> list[int]:
    """
    Find two numbers that sum to target in a sorted array.
    Pattern: Two Pointers
    Time: O(n)
    Space: O(1)
    """
    left, right = 0, len(nums) - 1

    while left < right:
        current_sum = nums[left] + nums[right]
        if current_sum == target:
            return [left, right]
        elif current_sum < target:
            left += 1
        else:
            right -= 1

    return []

if __name__ == "__main__":
    # Test cases
    assert two_sum_sorted([2, 7, 11, 15], 9) == [0, 1]
    assert two_sum_sorted([2, 3, 4], 6) == [0, 2]
    assert two_sum_sorted([-1, 0], -1) == [0, 1]
    print("All tests passed!")
