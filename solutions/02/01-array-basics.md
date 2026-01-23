# Array Basics

## Practice Problems

### 1. Rotate Array
**Difficulty:** Medium
**Key Concept:** Reversal trick

```python
def rotate(nums: list[int], k: int) -> None:
    """
    Rotates the array to the right by k steps in-place.
    Time: O(n)
    Space: O(1)
    """
    n = len(nums)
    k %= n

    def reverse(l: int, r: int) -> None:
        while l < r:
            nums[l], nums[r] = nums[r], nums[l]
            l += 1
            r -= 1

    reverse(0, n - 1)
    reverse(0, k - 1)
    reverse(k, n - 1)
```

### 2. Plus One
**Difficulty:** Easy
**Key Concept:** Carry propagation

```python
def plus_one(digits: list[int]) -> list[int]:
    """
    Increments the large integer represented by digits by one.
    Time: O(n)
    Space: O(1) (excluding result if new list)
    """
    n = len(digits)
    for i in range(n - 1, -1, -1):
        if digits[i] < 9:
            digits[i] += 1
            return digits
        digits[i] = 0
    return [1] + digits
```

### 3. Move Zeroes
**Difficulty:** Easy
**Key Concept:** Two pointers

```python
def move_zeroes(nums: list[int]) -> None:
    """
    Moves all 0's to the end while maintaining relative order of non-zeros.
    Time: O(n)
    Space: O(1)
    """
    slow = 0
    for fast in range(len(nums)):
        if nums[fast] != 0:
            nums[slow], nums[fast] = nums[fast], nums[slow]
            slow += 1
```

### 4. Remove Element
**Difficulty:** Easy
**Key Concept:** In-place modification

```python
def remove_element(nums: list[int], val: int) -> int:
    """
    Removes all occurrences of val in-place. Returns new length.
    Time: O(n)
    Space: O(1)
    """
    slow = 0
    for fast in range(len(nums)):
        if nums[fast] != val:
            nums[slow] = nums[fast]
            slow += 1
    return slow
```

### 5. Find All Duplicates in an Array
**Difficulty:** Medium
**Key Concept:** Index as hash

```python
def find_duplicates(nums: list[int]) -> list[int]:
    """
    Finds all elements that appear twice using O(1) extra space.
    Time: O(n)
    Space: O(1) (result excluded)
    """
    res = []
    for num in nums:
        idx = abs(num) - 1
        if nums[idx] < 0:
            res.append(idx + 1)
        else:
            nums[idx] = -nums[idx]
    return res
```

### 6. Product of Array Except Self
**Difficulty:** Medium
**Key Concept:** Prefix/suffix products

```python
def product_except_self(nums: list[int]) -> list[int]:
    """
    Returns array where each element is product of all others except self.
    Time: O(n)
    Space: O(1) (result excluded)
    """
    n = len(nums)
    res = [1] * n

    # Prefix products
    prefix = 1
    for i in range(n):
        res[i] = prefix
        prefix *= nums[i]

    # Suffix products
    suffix = 1
    for i in range(n - 1, -1, -1):
        res[i] *= suffix
        suffix *= nums[i]

    return res
```
