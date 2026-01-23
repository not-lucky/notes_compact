# In-Place Modifications

## Practice Problems

### 1. Move Zeroes
**Difficulty:** Easy
**Technique:** Two pointers

```python
def move_zeroes(nums: list[int]) -> None:
    """
    Time: O(n)
    Space: O(1)
    """
    slow = 0
    for fast in range(len(nums)):
        if nums[fast] != 0:
            nums[slow], nums[fast] = nums[fast], nums[slow]
            slow += 1
```

### 2. Remove Element
**Difficulty:** Easy
**Technique:** Two pointers

```python
def remove_element(nums: list[int], val: int) -> int:
    """
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

### 3. Remove Duplicates from Sorted Array
**Difficulty:** Easy
**Technique:** Two pointers

```python
def remove_duplicates(nums: list[int]) -> int:
    """
    Time: O(n)
    Space: O(1)
    """
    if not nums: return 0
    slow = 0
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]
    return slow + 1
```

### 4. Sort Colors
**Difficulty:** Medium
**Technique:** Dutch flag

```python
def sort_colors(nums: list[int]) -> None:
    """
    Time: O(n)
    Space: O(1)
    """
    l, m, h = 0, 0, len(nums) - 1
    while m <= h:
        if nums[m] == 0:
            nums[l], nums[m] = nums[m], nums[l]
            l += 1; m += 1
        elif nums[m] == 1:
            m += 1
        else:
            nums[m], nums[h] = nums[h], nums[m]
            h -= 1
```

### 5. Rotate Array
**Difficulty:** Medium
**Technique:** Reversal trick

```python
def rotate(nums: list[int], k: int) -> None:
    """
    Time: O(n)
    Space: O(1)
    """
    n = len(nums)
    k %= n
    def rev(l, r):
        while l < r:
            nums[l], nums[r] = nums[r], nums[l]
            l += 1; r -= 1
    rev(0, n-1)
    rev(0, k-1)
    rev(k, n-1)
```

### 6. Next Permutation
**Difficulty:** Medium
**Technique:** Find pivot, swap, reverse

```python
def next_permutation(nums: list[int]) -> None:
    """
    Time: O(n)
    Space: O(1)
    """
    i = len(nums) - 2
    while i >= 0 and nums[i] >= nums[i+1]:
        i -= 1
    if i >= 0:
        j = len(nums) - 1
        while nums[j] <= nums[i]:
            j -= 1
        nums[i], nums[j] = nums[j], nums[i]

    l, r = i + 1, len(nums) - 1
    while l < r:
        nums[l], nums[r] = nums[r], nums[l]
        l += 1; r -= 1
```

### 7. Find All Duplicates in Array
**Difficulty:** Medium
**Technique:** Index encoding

```python
def find_duplicates(nums: list[int]) -> list[int]:
    """
    Time: O(n)
    Space: O(1)
    """
    res = []
    for n in nums:
        idx = abs(n) - 1
        if nums[idx] < 0:
            res.append(idx + 1)
        else:
            nums[idx] *= -1
    return res
```

### 8. Wiggle Sort II
**Difficulty:** Medium
**Technique:** Virtual indexing

```python
def wiggle_sort(nums: list[int]) -> None:
    """
    Time: O(n)
    Space: O(1) (with median finding)
    """
    n = len(nums)
    copy = sorted(nums)
    mid = (n - 1) // 2
    end = n - 1
    for i in range(n):
        if i % 2 == 0:
            nums[i] = copy[mid]
            mid -= 1
        else:
            nums[i] = copy[end]
            end -= 1
```
