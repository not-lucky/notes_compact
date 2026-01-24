# Two Pointers: Same Direction - Solutions

## Practice Problems

### 1. Remove Duplicates from Sorted Array
**Problem Statement**: Given an integer array `nums` sorted in non-decreasing order, remove the duplicates in-place such that each unique element appears only once. The relative order of the elements should be kept the same. Then return the number of unique elements in `nums`.

**Examples & Edge Cases**:
- Example 1: `nums = [1,1,2]` -> `k = 2, nums = [1,2,_]`
- Example 2: `nums = [0,0,1,1,1,2,2,3,3,4]` -> `k = 5, nums = [0,1,2,3,4,_,_,_,_,_]`
- Edge Case: Empty array.
- Edge Case: No duplicates.
- Edge Case: All elements are the same.

**Optimal Python Solution**:
```python
def removeDuplicates(nums: list[int]) -> int:
    if not nums:
        return 0

    # slow pointer marks the position of the last unique element found
    slow = 0

    # fast pointer scans the array
    for fast in range(1, len(nums)):
        # If current element is different from the last unique element
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]

    return slow + 1
```

**Explanation**:
We use a slow pointer `slow` to keep track of the index of the last unique element placed. The `fast` pointer iterates through the array starting from the second element. Whenever `nums[fast]` is different from `nums[slow]`, it means we found a new unique element. We increment `slow` and copy the new unique element to that position.

**Complexity Analysis**:
- **Time Complexity**: O(n), where n is the length of the array. We traverse the array once.
- **Space Complexity**: O(1), as we modify the array in-place.

---

### 2. Remove Duplicates from Sorted Array II
**Problem Statement**: Given an integer array `nums` sorted in non-decreasing order, remove some duplicates in-place such that each unique element appears at most twice. The relative order of the elements should be kept the same. Return the new length.

**Examples & Edge Cases**:
- Example 1: `nums = [1,1,1,2,2,3]` -> `k = 5, nums = [1,1,2,2,3,_]`
- Example 2: `nums = [0,0,1,1,1,1,2,3,3]` -> `k = 7, nums = [0,0,1,1,2,3,3,_,_]`
- Edge Case: Array length <= 2.
- Edge Case: All elements are the same.

**Optimal Python Solution**:
```python
def removeDuplicates(nums: list[int]) -> int:
    # If array has 2 or fewer elements, it already satisfies the condition
    if len(nums) <= 2:
        return len(nums)

    # slow pointer marks the next position to write to
    # The first two elements are always kept
    slow = 2

    for fast in range(2, len(nums)):
        # Compare current element with the element two positions before the write head
        if nums[fast] != nums[slow - 2]:
            nums[slow] = nums[fast]
            slow += 1

    return slow
```

**Explanation**:
The condition "at most twice" means an element `nums[fast]` can be kept if it's different from `nums[slow-2]`. If `nums[fast] == nums[slow-2]`, and since the array is sorted, it implies `nums[slow-2] == nums[slow-1] == nums[fast]`, which would be three of the same kind. By checking against `slow-2`, we automatically allow up to two occurrences.

**Complexity Analysis**:
- **Time Complexity**: O(n), where n is the length of the array.
- **Space Complexity**: O(1), in-place modification.

---

### 3. Move Zeroes
**Problem Statement**: Move all `0`'s to the end of an array while maintaining the relative order of non-zero elements.

**Examples & Edge Cases**:
- Example 1: `[0,1,0,3,12]` -> `[1,3,12,0,0]`
- Edge Case: Array with no zeros.
- Edge Case: Array with only zeros.

**Optimal Python Solution**:
```python
def moveZeroes(nums: list[int]) -> None:
    # slow tracks the position to place the next non-zero element
    slow = 0
    for fast in range(len(nums)):
        if nums[fast] != 0:
            # Swap non-zero element with the element at the 'slow' position
            nums[slow], nums[fast] = nums[fast], nums[slow]
            slow += 1
```

**Explanation**:
By swapping the current element with the element at the `slow` pointer whenever we see a non-zero, we naturally "pull" non-zeros to the front and "push" zeros to the back.

**Complexity Analysis**:
- **Time Complexity**: O(n), single pass.
- **Space Complexity**: O(1), in-place.

---

### 4. Remove Element
**Problem Statement**: Remove all occurrences of `val` in `nums` in-place and return the number of elements not equal to `val`.

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

**Explanation**:
`fast` explores the array. If `nums[fast]` is not the target value, we "write" it to the `slow` index and increment `slow`.

**Complexity Analysis**:
- **Time Complexity**: O(n).
- **Space Complexity**: O(1).

---

### 5. Sort Colors (Dutch Flag Problem)
**Problem Statement**: Given an array `nums` with `n` objects colored red, white, or blue, sort them in-place so that objects of the same color are adjacent, with the colors in the order red (0), white (1), and blue (2).

**Examples & Edge Cases**:
- Example 1: `[2,0,2,1,1,0]` -> `[0,0,1,1,2,2]`
- Edge Case: Array with only one color.
- Edge Case: Empty array.

**Optimal Python Solution**:
```python
def sortColors(nums: list[int]) -> None:
    # Three pointers: low (boundary for 0s), high (boundary for 2s), and curr
    low = 0
    curr = 0
    high = len(nums) - 1

    while curr <= high:
        if nums[curr] == 0:
            # Found a 0, move to the front
            nums[low], nums[curr] = nums[curr], nums[low]
            low += 1
            curr += 1
        elif nums[curr] == 2:
            # Found a 2, move to the back
            nums[high], nums[curr] = nums[curr], nums[high]
            high -= 1
            # Note: Do not increment curr here, as the new nums[curr] needs checking
        else:
            # Found a 1, just move forward
            curr += 1
```

**Explanation**:
This is the classic Dutch National Flag algorithm. We maintain three sections: `[0, low)` for 0s, `[low, curr)` for 1s, and `(high, n-1]` for 2s. Elements between `curr` and `high` are unprocessed.
- If we see a 0, we swap it with `low` and advance both `low` and `curr`.
- If we see a 2, we swap it with `high` and decrement `high`. We don't advance `curr` because the swapped element from `high` could be a 0 or 1 that needs processing.
- If we see a 1, we just advance `curr`.

**Complexity Analysis**:
- **Time Complexity**: O(n), single pass through the array.
- **Space Complexity**: O(1), in-place swaps.

---

### 6. Squares of a Sorted Array
**Problem Statement**: Given an integer array `nums` sorted in non-decreasing order, return an array of the squares of each number sorted in non-decreasing order.

**Examples & Edge Cases**:
- Example 1: `[-4,-1,0,3,10]` -> `[0,1,9,16,100]`
- Example 2: `[-7,-3,2,3,11]` -> `[4,9,9,49,121]`
- Edge Case: All negative numbers.
- Edge Case: All positive numbers.

**Optimal Python Solution**:
```python
def sortedSquares(nums: list[int]) -> list[int]:
    n = len(nums)
    result = [0] * n
    left = 0
    right = n - 1

    # Fill result from the end (largest values)
    for i in range(n - 1, -1, -1):
        if abs(nums[left]) > abs(nums[right]):
            result[i] = nums[left] ** 2
            left += 1
        else:
            result[i] = nums[right] ** 2
            right -= 1

    return result
```

**Explanation**:
Since the input is sorted, the largest squares will come from either the far left (most negative) or the far right (most positive). We use two pointers at the ends and compare their absolute values. The larger absolute value's square is placed at the end of the result array, and the corresponding pointer is moved.

**Complexity Analysis**:
- **Time Complexity**: O(n), we visit each element exactly once.
- **Space Complexity**: O(n) for the output array (or O(1) if output is not counted).

---

### 7. Linked List Cycle
**Problem Statement**: Given `head`, the head of a linked list, determine if the linked list has a cycle in it.

**Examples & Edge Cases**:
- Example: `head = [3,2,0,-4], pos = 1` -> `true`
- Edge Case: Single node with no cycle.
- Edge Case: Empty list.

**Optimal Python Solution**:
```python
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

def hasCycle(head: ListNode) -> bool:
    if not head:
        return False

    slow = head
    fast = head

    while fast and fast.next:
        slow = slow.next          # Move 1 step
        fast = fast.next.next     # Move 2 steps

        if slow == fast:
            return True           # Cycle detected

    return False
```

**Explanation**:
This is Floyd's Cycle-Finding Algorithm (Tortoise and Hare). We use two pointers moving at different speeds. If there is a cycle, the fast pointer will eventually "lap" the slow pointer and they will meet. If there is no cycle, the fast pointer will reach the end of the list.

**Complexity Analysis**:
- **Time Complexity**: O(n). In the worst case (no cycle), we traverse once. If there is a cycle, the fast pointer catches the slow pointer in at most `n` steps.
- **Space Complexity**: O(1), only two pointers used.
