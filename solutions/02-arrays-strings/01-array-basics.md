# Array Basics - Solutions

## Practice Problems

### 1. Rotate Array

**Problem Statement**: Given an integer array `nums`, rotate the array to the right by `k` steps, where `k` is non-negative.

**Examples & Edge Cases**:

- Example 1: `nums = [1,2,3,4,5,6,7], k = 3` -> `[5,6,7,1,2,3,4]`
- Example 2: `nums = [-1,-100,3,99], k = 2` -> `[3,99,-1,-100]`
- Edge Case: `k` is greater than the length of the array (`k = k % n`).
- Edge Case: Empty array or array with one element.
- Edge Case: `k = 0`, no rotation needed.

**Optimal Python Solution**:

```python
def rotate(nums: list[int], k: int) -> None:
    """
    Do not return anything, modify nums in-place instead.
    """
    n = len(nums)
    if n == 0:
        return

    k = k % n
    if k == 0:
        return

    def reverse(left: int, right: int) -> None:
        while left < right:
            nums[left], nums[right] = nums[right], nums[left]
            left += 1
            right -= 1

    # 1. Reverse the entire array
    reverse(0, n - 1)
    # 2. Reverse the first k elements
    reverse(0, k - 1)
    # 3. Reverse the remaining n-k elements
    reverse(k, n - 1)
```

**Explanation**:
The "reversal trick" is an elegant way to rotate an array in-place with O(1) extra space.

1. Reversing the entire array brings the elements that should be at the front to the front, but in reverse order.
2. Reversing the first `k` elements restores their original relative order.
3. Reversing the remaining `n-k` elements restores their original relative order.

**Complexity Analysis**:

- **Time Complexity**: O(n), where n is the length of the array. We perform three reversal passes, each visiting elements at most twice.
- **Space Complexity**: O(1), as we modify the array in-place and only use a few variables for pointers.

---

### 2. Plus One

**Problem Statement**: You are given a large integer represented as an integer array `digits`, where each `digits[i]` is the `i-th` digit of the integer. The digits are ordered from most significant to least significant in left-to-right order. The large integer does not contain any leading 0's. Increment the large integer by one and return the resulting array of digits.

**Examples & Edge Cases**:

- Example 1: `digits = [1,2,3]` -> `[1,2,4]`
- Example 2: `digits = [4,3,2,1]` -> `[4,3,2,2]`
- Example 3: `digits = [9]` -> `[1,0]`
- Edge Case: All digits are 9 (e.g., `[9,9,9]` -> `[1,0,0,0]`).
- Edge Case: Single digit `0`.

**Optimal Python Solution**:

```python
def plusOne(digits: list[int]) -> list[int]:
    n = len(digits)

    # Traverse from right to left
    for i in range(n - 1, -1, -1):
        if digits[i] < 9:
            # If digit is less than 9, just increment and return
            digits[i] += 1
            return digits
        # If digit is 9, it becomes 0 and carry continues
        digits[i] = 0

    # If we finish the loop, it means we had all 9s (e.g., 999 -> 1000)
    return [1] + digits
```

**Explanation**:
We start from the least significant digit (the end of the array). If a digit is less than 9, incrementing it won't produce a carry that affects the next digit, so we can stop immediately. If a digit is 9, it becomes 0, and we move to the next more significant digit. If all digits were 9, we end up with an array of 0s and need to prepend a 1.

**Complexity Analysis**:

- **Time Complexity**: O(n) in the worst case (e.g., `[9,9,9]`), where n is the number of digits. Usually, it's O(1) on average.
- **Space Complexity**: O(n) in the worst case if we create a new array (the `[1] + digits` case), otherwise O(1) if we modify in-place.

---

### 3. Move Zeroes

**Problem Statement**: Given an integer array `nums`, move all `0`'s to the end of it while maintaining the relative order of the non-zero elements. Note that you must do this in-place without making a copy of the array.

**Examples & Edge Cases**:

- Example 1: `nums = [0,1,0,3,12]` -> `[1,3,12,0,0]`
- Example 2: `nums = [0]` -> `[0]`
- Edge Case: All zeroes.
- Edge Case: No zeroes.
- Edge Case: Array already correctly formatted.

**Optimal Python Solution**:

```python
def moveZeroes(nums: list[int]) -> None:
    """
    Do not return anything, modify nums in-place instead.
    """
    # last_non_zero_found_at tracks the position to place the next non-zero element
    last_non_zero_found_at = 0

    for i in range(len(nums)):
        if nums[i] != 0:
            # Swap current non-zero element with the element at the tracking pointer
            nums[last_non_zero_found_at], nums[i] = nums[i], nums[last_non_zero_found_at]
            last_non_zero_found_at += 1
```

**Explanation**:
We use a two-pointer approach. The `last_non_zero_found_at` pointer tracks where the next non-zero element should be placed. As we iterate through the array with `i`, whenever we encounter a non-zero element, we swap it with the element at `last_non_zero_found_at` and increment the pointer. This effectively pushes zeroes to the right and pulls non-zeroes to the left while maintaining order.

**Complexity Analysis**:

- **Time Complexity**: O(n), where n is the length of the array. We traverse the array once.
- **Space Complexity**: O(1), as we only use one additional integer variable for the pointer.

---

### 4. Remove Element

**Problem Statement**: Given an integer array `nums` and an integer `val`, remove all occurrences of `val` in `nums` in-place. The order of the elements may be changed. Then return the number of elements in `nums` which are not equal to `val`.

**Examples & Edge Cases**:

- Example 1: `nums = [3,2,2,3], val = 3` -> `k = 2, nums = [2,2,_,_]`
- Example 2: `nums = [0,1,2,2,3,0,4,2], val = 2` -> `k = 5, nums = [0,1,3,0,4,_,_,_]`
- Edge Case: Array is empty.
- Edge Case: All elements are equal to `val`.
- Edge Case: No elements are equal to `val`.

**Optimal Python Solution**:

```python
def removeElement(nums: list[int], val: int) -> int:
    # k tracks the count/index of elements not equal to val
    k = 0
    for i in range(len(nums)):
        if nums[i] != val:
            nums[k] = nums[i]
            k += 1
    return k
```

**Explanation**:
Similar to "Move Zeroes", we use a slow-runner pointer `k` and a fast-runner pointer `i`. `i` iterates through all elements. Whenever `nums[i]` is not the value to be removed, we copy it to `nums[k]` and increment `k`. The first `k` elements of the modified array will be the elements not equal to `val`.

**Complexity Analysis**:

- **Time Complexity**: O(n), where n is the length of the array. We traverse the array once.
- **Space Complexity**: O(1), as we only use one extra integer variable.

---

### 5. Find All Duplicates in an Array

**Problem Statement**: Given an integer array `nums` of length `n` where all the integers of `nums` are in the range `[1, n]` and each integer appears once or twice, return an array of all the integers that appears twice. You must write an algorithm that runs in O(n) time and uses only constant extra space.

**Examples & Edge Cases**:

- Example 1: `nums = [4,3,2,7,8,2,3,1]` -> `[2,3]`
- Example 2: `nums = [1,1,2]` -> `[1]`
- Example 3: `nums = [1]` -> `[]`
- Edge Case: No duplicates.
- Edge Case: All elements have a duplicate.

**Optimal Python Solution**:

```python
def findDuplicates(nums: list[int]) -> list[int]:
    result = []

    for x in nums:
        # Use the value as an index (mapped from 1..n to 0..n-1)
        index = abs(x) - 1

        # If the value at that index is negative, we've seen this number before
        if nums[index] < 0:
            result.append(abs(x))
        else:
            # Mark the value at that index as visited by making it negative
            nums[index] = -nums[index]

    return result
```

**Explanation**:
Since the numbers are in the range `[1, n]`, we can use the array itself as a hash table. For each number `x` we encounter, we go to the index `abs(x) - 1`. If the value at that index is positive, we flip it to negative to mark it as "seen". If it's already negative, it means we've encountered `x` before, so `x` is a duplicate.

**Complexity Analysis**:

- **Time Complexity**: O(n), where n is the length of the array. We iterate through the array once.
- **Space Complexity**: O(1) extra space (excluding the output list), as we modify the input array in-place.

---

### 6. Product of Array Except Self

**Problem Statement**: Given an integer array `nums`, return an array `answer` such that `answer[i]` is equal to the product of all the elements of `nums` except `nums[i]`. The algorithm must run in O(n) time and without using the division operation.

**Examples & Edge Cases**:

- Example 1: `nums = [1,2,3,4]` -> `[24,12,8,6]`
- Example 2: `nums = [-1,1,0,-3,3]` -> `[0,0,9,0,0]`
- Edge Case: Array contains one or more zeroes.
- Edge Case: Array contains negative numbers.

**Optimal Python Solution**:

```python
def productExceptSelf(nums: list[int]) -> list[int]:
    n = len(nums)
    res = [1] * n

    # Prefix products: res[i] contains product of all elements to the left of i
    prefix = 1
    for i in range(n):
        res[i] = prefix
        prefix *= nums[i]

    # Suffix products: multiply res[i] by product of all elements to the right of i
    suffix = 1
    for i in range(n - 1, -1, -1):
        res[i] *= suffix
        suffix *= nums[i]

    return res
```

**Explanation**:
To calculate the product of everything except `nums[i]`, we need the product of everything to the left of `i` and everything to the right of `i`.

1. We first pass forward to calculate prefix products.
2. We then pass backward to calculate suffix products and multiply them with the corresponding prefix products already stored in the result array.

**Complexity Analysis**:

- **Time Complexity**: O(n), where n is the length of the array. We perform two linear passes.
- **Space Complexity**: O(1) extra space, if we don't count the output array (as per common interview evaluation).
