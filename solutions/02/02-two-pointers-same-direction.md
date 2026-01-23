# Two Pointers: Same Direction

## Practice Problems

### 1. Remove Duplicates from Sorted Array
**Difficulty:** Easy
**Pattern:** Basic slow/fast

```python
def remove_duplicates(nums: list[int]) -> int:
    """
    Removes duplicates from sorted array in-place.
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

### 2. Remove Duplicates from Sorted Array II
**Difficulty:** Medium
**Pattern:** Allow k duplicates

```python
def remove_duplicates_ii(nums: list[int]) -> int:
    """
    Allows each element at most twice.
    Time: O(n)
    Space: O(1)
    """
    if len(nums) <= 2: return len(nums)
    slow = 2
    for fast in range(2, len(nums)):
        if nums[fast] != nums[slow - 2]:
            nums[slow] = nums[fast]
            slow += 1
    return slow
```

### 3. Move Zeroes
**Difficulty:** Easy
**Pattern:** Partition

```python
def move_zeroes(nums: list[int]) -> None:
    """
    Moves zeroes to end while maintaining order.
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
**Pattern:** Filter in-place

```python
def remove_element(nums: list[int], val: int) -> int:
    """
    Removes all occurrences of val.
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

### 5. Sort Colors (Dutch Flag)
**Difficulty:** Medium
**Pattern:** Three-way partition

```python
def sort_colors(nums: list[int]) -> None:
    """
    Sorts 0s, 1s, and 2s in-place.
    Time: O(n)
    Space: O(1)
    """
    low, mid, high = 0, 0, len(nums) - 1
    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1
```

### 6. Squares of a Sorted Array
**Difficulty:** Easy
**Pattern:** Fill from ends

```python
def sorted_squares(nums: list[int]) -> list[int]:
    """
    Returns sorted squares of a sorted array.
    Time: O(n)
    Space: O(n)
    """
    n = len(nums)
    res = [0] * n
    l, r = 0, n - 1
    for i in range(n - 1, -1, -1):
        if abs(nums[l]) > abs(nums[r]):
            res[i] = nums[l] ** 2
            l += 1
        else:
            res[i] = nums[r] ** 2
            r -= 1
    return res
```

### 7. Linked List Cycle
**Difficulty:** Easy
**Pattern:** Fast/slow pointers

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

def hasCycle(head) -> bool:
    """
    Detects if a linked list has a cycle.
    Time: O(n)
    Space: O(1)
    """
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False
```
