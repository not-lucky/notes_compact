# Solutions: Intersection Detection

## 1. Intersection of Two Linked Lists

**Problem Statement**: Given the heads of two singly linked-lists `headA` and `headB`, return the node at which the two lists intersect. If the two linked lists have no intersection at all, return `null`.

### Examples & Edge Cases

- **Example 1**: `listA = [4,1,8,4,5], listB = [5,6,1,8,4,5]`. Intersection at node with value 8.
- **Example 2**: `listA = [1,9,1,2,4], listB = [3,2,4]`. Intersection at node with value 2.
- **Example 3**: `listA = [2,6,4], listB = [1,5]`. No intersection (return `null`).
- **Edge Case**: One or both lists are empty.
- **Edge Case**: Intersection occurs at the very first node (the lists are the same).
- **Edge Case**: Intersection occurs at the very last node.

### Optimal Python Solution

```python
def getIntersectionNode(headA: ListNode, headB: ListNode) -> ListNode:
    """
    Two-pointer technique to equalize travel distance.
    If they intersect, they will meet at the intersection point.
    If they don't, they will both hit None at the same time.
    """
    if not headA or not headB:
        return None

    ptrA = headA
    ptrB = headB

    # Loop until the two pointers meet
    while ptrA != ptrB:
        # If ptrA reaches the end, switch to headB
        ptrA = ptrA.next if ptrA else headB
        # If ptrB reaches the end, switch to headA
        ptrB = ptrB.next if ptrB else headA

    # When they meet, it's either the intersection node or None (end of both)
    return ptrA
```

### Explanation

The core idea is that both pointers will travel the same total distance.

- Pointer A travels: `Length(A) + Length(B_unique_part)`
- Pointer B travels: `Length(B) + Length(A_unique_part)`
  Since `Length(A) + Length(B_unique_part) == Length(B) + Length(A_unique_part)`, they must meet at the intersection node or at `null` simultaneously. This handles different list lengths perfectly in O(1) space.

### Complexity Analysis

- **Time Complexity**: O(n + m), where `n` and `m` are the lengths of the two lists. Each pointer traverses at most two lists.
- **Space Complexity**: O(1). Only two pointers are used.

---

## 2. Find the Duplicate Number

**Problem Statement**: Given an array of integers `nums` containing `n + 1` integers where each integer is in the range `[1, n]` inclusive. There is only one repeated number in `nums`, return this repeated number. You must solve the problem without modifying the array `nums` and uses only constant extra space.

### Examples & Edge Cases

- **Example 1**: `nums = [1,3,4,2,2]` -> `2`
- **Example 2**: `nums = [3,1,3,4,2]` -> `3`
- **Edge Case**: `nums = [1,1]` -> `1`
- **Edge Case**: `nums = [1,1,2]` -> `1`

### Optimal Python Solution

```python
def findDuplicate(nums: list[int]) -> int:
    """
    Treat the array as a linked list where nums[i] is the next pointer.
    The problem becomes finding the entrance to a cycle (Floyd's).
    """
    # Phase 1: Finding the intersection point in the cycle
    slow = nums[0]
    fast = nums[nums[0]]

    while slow != fast:
        slow = nums[slow]
        fast = nums[nums[fast]]

    # Phase 2: Finding the entrance of the cycle
    slow = 0
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]

    return slow
```

### Explanation

Because each number is in the range `[1, n]` and there are `n+1` numbers, we can treat the value at each index as a "pointer" to another index. Since there is a duplicate, multiple indices will point to the same value, creating a cycle. Finding the duplicate is equivalent to finding the start of this cycle.

### Complexity Analysis

- **Time Complexity**: O(n). We use Floyd's cycle-finding algorithm which is linear.
- **Space Complexity**: O(1). We do not use any extra space or modify the input.
