# In-Place Modifications - Solutions

## Practice Problems

### 1. Move Zeroes

**Problem Statement**: Given an integer array `nums`, move all `0`'s to the end of it while maintaining the relative order of the non-zero elements.

**Optimal Python Solution**:

```python
def moveZeroes(nums: list[int]) -> None:
    # slow pointer tracks the position to place the next non-zero element
    slow = 0
    for fast in range(len(nums)):
        if nums[fast] != 0:
            # Swap non-zero element with the element at the tracking pointer
            nums[slow], nums[fast] = nums[fast], nums[slow]
            slow += 1
```

**Complexity Analysis**:

- **Time Complexity**: O(n).
- **Space Complexity**: O(1).

---

### 2. Remove Element

**Problem Statement**: Given an integer array `nums` and an integer `val`, remove all occurrences of `val` in `nums` in-place.

**Optimal Python Solution**:

```python
def removeElement(nums: list[int], val: int) -> int:
    slow = 0
    for fast in range(len(nums)):
        if nums[fast] != val:
            nums[slow] = nums[fast]
            slow += 1
    return slow
```

**Complexity Analysis**:

- **Time Complexity**: O(n).
- **Space Complexity**: O(1).

---

### 3. Remove Duplicates from Sorted Array

**Problem Statement**: Remove duplicates from a sorted array in-place.

**Optimal Python Solution**:

```python
def removeDuplicates(nums: list[int]) -> int:
    if not nums: return 0
    slow = 0
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]
    return slow + 1
```

**Complexity Analysis**:

- **Time Complexity**: O(n).
- **Space Complexity**: O(1).

---

### 4. Sort Colors

**Problem Statement**: Sort an array containing 0s, 1s, and 2s in-place.

**Optimal Python Solution**:

```python
def sortColors(nums: list[int]) -> None:
    low = 0
    mid = 0
    high = len(nums) - 1

    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else: # nums[mid] == 2
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1
```

**Complexity Analysis**:

- **Time Complexity**: O(n).
- **Space Complexity**: O(1).

---

### 5. Rotate Array

**Problem Statement**: Rotate an array to the right by `k` steps.

**Optimal Python Solution**:

```python
def rotate(nums: list[int], k: int) -> None:
    n = len(nums)
    k %= n
    if k == 0: return

    def reverse(l, r):
        while l < r:
            nums[l], nums[r] = nums[r], nums[l]
            l += 1
            r -= 1

    # Reversal trick
    reverse(0, n - 1)
    reverse(0, k - 1)
    reverse(k, n - 1)
```

**Complexity Analysis**:

- **Time Complexity**: O(n).
- **Space Complexity**: O(1).

---

### 6. Next Permutation

**Problem Statement**: Implement next permutation, which rearranges numbers into the lexicographically next greater permutation of numbers.

**Optimal Python Solution**:

```python
def nextPermutation(nums: list[int]) -> None:
    n = len(nums)
    # 1. Find the first pair nums[i] < nums[i+1] from right
    i = n - 2
    while i >= 0 and nums[i] >= nums[i+1]:
        i -= 1

    if i >= 0:
        # 2. Find the smallest number in nums[i+1:] that is > nums[i]
        j = n - 1
        while j >= 0 and nums[j] <= nums[i]:
            j -= 1
        # 3. Swap them
        nums[i], nums[j] = nums[j], nums[i]

    # 4. Reverse the suffix nums[i+1:]
    left, right = i + 1, n - 1
    while left < right:
        nums[left], nums[right] = nums[right], nums[left]
        left += 1
        right -= 1
```

**Explanation**:
We find the "pivot" (the rightmost point where the array is not decreasing). We swap this pivot with the next largest element to its right, and then reverse the rest of the array to make the new suffix as small as possible.

**Complexity Analysis**:

- **Time Complexity**: O(n).
- **Space Complexity**: O(1).

---

### 7. Find All Duplicates in Array

**Problem Statement**: Given an array of integers where 1 ≤ `a[i]` ≤ n (n = size of array), some elements appear twice and others appear once. Find all the elements that appear twice in this array.

**Optimal Python Solution**:

```python
def findDuplicates(nums: list[int]) -> list[int]:
    res = []
    for x in nums:
        # Index encoding trick: negate the value at index abs(x)-1
        idx = abs(x) - 1
        if nums[idx] < 0:
            res.append(abs(x))
        else:
            nums[idx] *= -1
    return res
```

**Explanation**:
Since elements are in range `[1, n]`, we can use the array itself as a frequency tracker. We negate the value at the index corresponding to each number. If we encounter a number whose corresponding index already has a negative value, it's a duplicate.

**Complexity Analysis**:

- **Time Complexity**: O(n).
- **Space Complexity**: O(1) extra space.

---

### 8. Wiggle Sort II

**Problem Statement**: Given an integer array `nums`, reorder it such that `nums[0] < nums[1] > nums[2] < nums[3]...`.

**Optimal Python Solution**:

```python
def wiggleSort(nums: list[int]) -> None:
    # A simple but optimal O(n log n) solution
    # For O(n) time and O(1) space, 3-way partitioning with virtual indexing is needed.
    nums.sort()
    half = (len(nums) + 1) // 2
    # Create copies to allow filling in-place correctly
    s1 = nums[:half]
    s2 = nums[half:]

    # Interleave from the end of sorted halves to handle duplicates correctly
    # nums[::2] are even indices, nums[1::2] are odd indices
    nums[::2] = s1[::-1]
    nums[1::2] = s2[::-1]
```

**Explanation**:
By sorting the array and splitting it into two halves, we can interleave them. Taking elements from the end of each half helps handle cases with many identical elements that would otherwise be adjacent.

**Complexity Analysis**:

- **Time Complexity**: O(n log n) due to sorting.
- **Space Complexity**: O(n) for the intermediate halves.
