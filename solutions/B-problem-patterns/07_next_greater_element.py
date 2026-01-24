def next_greater_element(nums: list[int]) -> list[int]:
    """
    Find next greater element for each element in array.
    Pattern: Monotonic Stack
    Time: O(n)
    Space: O(n)
    """
    n = len(nums)
    result = [-1] * n
    stack = []  # Store indices

    for i in range(n):
        # While current element is greater than element at index on top of stack
        while stack and nums[i] > nums[stack[-1]]:
            prev_index = stack.pop()
            result[prev_index] = nums[i]
        stack.append(i)

    return result

if __name__ == "__main__":
    # Test cases
    assert next_greater_element([1, 2, 1]) == [2, -1, -1]
    assert next_greater_element([4, 5, 2, 25]) == [5, 25, 25, -1]
    assert next_greater_element([13, 7, 6, 12]) == [-1, 12, 12, -1]
    print("All tests passed!")
