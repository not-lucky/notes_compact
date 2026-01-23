# Solution: Dummy Node Technique Practice Problems

## Problem 1: Remove Linked List Elements
### Problem Statement
Given the head of a linked list and an integer `val`, remove all the nodes of the linked list that has `Node.val == val`, and return the new head.

### Constraints
- The number of nodes in the list is in the range `[0, 10^4]`.
- `1 <= Node.val <= 50`
- `0 <= val <= 50`

### Example
Input: `head = [1,2,6,3,4,5,6], val = 6`
Output: `[1,2,3,4,5]`

### Python Implementation
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def removeElements(head: ListNode, val: int) -> ListNode:
    """
    Time Complexity: O(n)
    Space Complexity: O(1)

    Use a dummy node to handle the case where the head itself needs to be removed.
    """
    dummy = ListNode(0)
    dummy.next = head
    curr = dummy

    while curr.next:
        if curr.next.val == val:
            curr.next = curr.next.next
        else:
            curr = curr.next

    return dummy.next
```

---

## Problem 2: Remove Nth Node From End
### Problem Statement
Given the head of a linked list, remove the nth node from the end of the list and return its head.

### Constraints
- The number of nodes in the list is `sz`.
- `1 <= sz <= 30`
- `0 <= Node.val <= 100`
- `1 <= n <= sz`

### Example
Input: `head = [1,2,3,4,5], n = 2`
Output: `[1,2,3,5]`

### Python Implementation
```python
def removeNthFromEnd(head: ListNode, n: int) -> ListNode:
    """
    Time Complexity: O(n)
    Space Complexity: O(1)

    Using dummy node handles the case where head needs to be removed (n = length).
    """
    dummy = ListNode(0, head)
    fast = slow = dummy

    for _ in range(n + 1):
        fast = fast.next

    while fast:
        slow = slow.next
        fast = fast.next

    slow.next = slow.next.next
    return dummy.next
```

---

## Problem 3: Partition List
### Problem Statement
Given the head of a linked list and a value `x`, partition it such that all nodes less than `x` come before nodes greater than or equal to `x`. You should preserve the original relative order of the nodes in each of the two partitions.

### Constraints
- The number of nodes in the list is in the range `[0, 200]`.
- `-100 <= Node.val <= 100`
- `-200 <= x <= 200`

### Example
Input: `head = [1,4,3,2,5,2], x = 3`
Output: `[1,2,2,4,3,5]`

### Python Implementation
```python
def partition(head: ListNode, x: int) -> ListNode:
    """
    Time Complexity: O(n)
    Space Complexity: O(1)

    Use two dummy nodes to build two separate lists and then connect them.
    """
    before_dummy = ListNode(0)
    after_dummy = ListNode(0)
    before = before_dummy
    after = after_dummy

    while head:
        if head.val < x:
            before.next = head
            before = before.next
        else:
            after.next = head
            after = after.next
        head = head.next

    after.next = None
    before.next = after_dummy.next

    return before_dummy.next
```

---

## Problem 4: Remove Duplicates from Sorted List II
### Problem Statement
Given the head of a sorted linked list, delete all nodes that have duplicate numbers, leaving only distinct numbers from the original list. Return the linked list sorted as well.

### Constraints
- The number of nodes in the list is in the range `[0, 300]`.
- `-100 <= Node.val <= 100`
- The list is guaranteed to be sorted in ascending order.

### Example
Input: `head = [1,2,3,3,4,4,5]`
Output: `[1,2,5]`

### Python Implementation
```python
def deleteDuplicates(head: ListNode) -> ListNode:
    """
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    dummy = ListNode(0, head)
    prev = dummy

    while head:
        if head.next and head.val == head.next.val:
            while head.next and head.val == head.next.val:
                head = head.next
            prev.next = head.next
        else:
            prev = prev.next
        head = head.next

    return dummy.next
```
