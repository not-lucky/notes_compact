# Solution: Intersection Detection Practice Problems

## Problem 1: Intersection of Two Linked Lists
### Problem Statement
Given the heads of two singly linked-lists `headA` and `headB`, return the node at which the two lists intersect. If the two linked lists have no intersection at all, return null.

### Constraints
- The number of nodes of `listA` is in the `m`.
- The number of nodes of `listB` is in the `n`.
- `1 <= m, n <= 3 * 10^4`
- `1 <= Node.val <= 10^5`
- `headA` and `headB` can be non-intersecting.

### Example
Input: `intersectVal = 8, listA = [4,1,8,4,5], listB = [5,6,1,8,4,5]`
Output: `Intersected at '8'`

### Python Implementation
```python
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

def getIntersectionNode(headA: ListNode, headB: ListNode) -> ListNode:
    """
    Time Complexity: O(n + m)
    Space Complexity: O(1)

    Each pointer traverses both lists. If they intersect, they will meet
    at the intersection point after at most (n+m) steps.
    """
    if not headA or not headB:
        return None

    pA, pB = headA, headB

    while pA != pB:
        pA = pA.next if pA else headB
        pB = pB.next if pB else headA

    return pA
```

---

## Problem 2: Find the Duplicate Number
### Problem Statement
Given an array of integers `nums` containing `n + 1` integers where each integer is in the range `[1, n]` inclusive. There is only one repeated number in `nums`, return this repeated number. You must solve the problem without modifying the array `nums` and uses only constant extra space.

### Constraints
- `1 <= n <= 10^5`
- `nums.length == n + 1`
- `1 <= nums[i] <= n`
- All the integers in `nums` appear only once except for precisely one integer which appears two or more times.

### Example
Input: `nums = [1,3,4,2,2]`
Output: `2`

### Python Implementation
```python
def findDuplicate(nums: list[int]) -> int:
    """
    Time Complexity: O(n)
    Space Complexity: O(1)

    Treat the array as a linked list where nums[i] points to index nums[i].
    The duplicate number will form a cycle. Use Floyd's Cycle Detection.
    """
    slow = nums[0]
    fast = nums[0]

    # Phase 1: Detect cycle
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break

    # Phase 2: Find cycle start
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]

    return slow
```
