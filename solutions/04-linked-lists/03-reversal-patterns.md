# Solution: Reversal Patterns Practice Problems

## Problem 1: Reverse Linked List
### Problem Statement
Given the head of a singly linked list, reverse the list, and return the reversed list.

### Constraints
- The number of nodes in the list is the range `[0, 5000]`.
- `-5000 <= Node.val <= 5000`

### Example
Input: `head = [1,2,3,4,5]`
Output: `[5,4,3,2,1]`

### Python Implementation
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverseList(head: ListNode) -> ListNode:
    """
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    prev = None
    curr = head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev
```

---

## Problem 2: Reverse Linked List II
### Problem Statement
Given the head of a singly linked list and two integers `left` and `right` where `left <= right`, reverse the nodes of the list from position `left` to position `right`, and return the reversed list.

### Constraints
- The number of nodes in the list is `n`.
- `1 <= n <= 500`
- `-500 <= Node.val <= 500`
- `1 <= left <= right <= n`

### Example
Input: `head = [1,2,3,4,5], left = 2, right = 4`
Output: `[1,4,3,2,5]`

### Python Implementation
```python
def reverseBetween(head: ListNode, left: int, right: int) -> ListNode:
    """
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    if not head or left == right:
        return head

    dummy = ListNode(0, head)
    before = dummy
    for _ in range(left - 1):
        before = before.next

    curr = before.next
    for _ in range(right - left):
        nxt = curr.next
        curr.next = nxt.next
        nxt.next = before.next
        before.next = nxt

    return dummy.next
```

---

## Problem 3: Swap Nodes in Pairs
### Problem Statement
Given a linked list, swap every two adjacent nodes and return its head. You must solve the problem without modifying the values in the list's nodes (i.e., only nodes themselves may be changed.)

### Constraints
- The number of nodes in the list is in the range `[0, 100]`.
- `0 <= Node.val <= 100`

### Example
Input: `head = [1,2,3,4]`
Output: `[2,1,4,3]`

### Python Implementation
```python
def swapPairs(head: ListNode) -> ListNode:
    """
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    dummy = ListNode(0, head)
    prev = dummy

    while prev.next and prev.next.next:
        first = prev.next
        second = prev.next.next

        # Swap
        first.next = second.next
        second.next = first
        prev.next = second

        # Move forward
        prev = first

    return dummy.next
```

---

## Problem 4: Reverse Nodes in k-Group
### Problem Statement
Given the head of a linked list, reverse the nodes of the list k at a time, and return the modified list. k is a positive integer and is less than or equal to the length of the linked list. If the number of nodes is not a multiple of k then left-out nodes, in the end, should remain as it is.

### Constraints
- The number of nodes in the list is `n`.
- `1 <= k <= n <= 5000`
- `0 <= Node.val <= 1000`

### Example
Input: `head = [1,2,3,4,5], k = 2`
Output: `[2,1,4,3,5]`

### Python Implementation
```python
def reverseKGroup(head: ListNode, k: int) -> ListNode:
    """
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    def reverse(start, end):
        prev = end
        curr = start
        while curr != end:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        return prev

    dummy = ListNode(0, head)
    prev = dummy

    while True:
        kth = prev
        for _ in range(k):
            kth = kth.next
            if not kth:
                return dummy.next

        nxt_group = kth.next
        first = prev.next
        prev.next = reverse(first, nxt_group)
        prev = first
```

---

## Problem 5: Rotate List
### Problem Statement
Given the head of a linked list, rotate the list to the right by k places.

### Constraints
- The number of nodes in the list is in the range `[0, 500]`.
- `-100 <= Node.val <= 100`
- `0 <= k <= 2 * 10^9`

### Example
Input: `head = [1,2,3,4,5], k = 2`
Output: `[4,5,1,2,3]`

### Python Implementation
```python
def rotateRight(head: ListNode, k: int) -> ListNode:
    """
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    if not head or not head.next or k == 0:
        return head

    # Find length and tail
    length = 1
    tail = head
    while tail.next:
        tail = tail.next
        length += 1

    k = k % length
    if k == 0:
        return head

    # Make it circular
    tail.next = head

    # Find new tail
    new_tail = head
    for _ in range(length - k - 1):
        new_tail = new_tail.next

    new_head = new_tail.next
    new_tail.next = None

    return new_head
```
