# Solution: Fast-Slow Pointers Practice Problems

## Problem 1: Middle of the Linked List
### Problem Statement
Given the head of a singly linked list, return the middle node of the linked list. If there are two middle nodes, return the second middle node.

### Constraints
- The number of nodes in the list is in the range `[1, 100]`.
- `1 <= Node.val <= 100`

### Example
Input: `head = [1,2,3,4,5]`
Output: `[3,4,5]`

### Python Implementation
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def middleNode(head: ListNode) -> ListNode:
    """
    Time Complexity: O(n)
    Space Complexity: O(1)

    Using fast and slow pointers. When fast reaches the end, slow is at the middle.
    """
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow
```

---

## Problem 2: Linked List Cycle
### Problem Statement
Given `head`, the head of a linked list, determine if the linked list has a cycle in it.

### Constraints
- The number of nodes in the list is in the range `[0, 10^4]`.
- `-10^5 <= Node.val <= 10^5`

### Example
Input: `head = [3,2,0,-4], pos = 1` (pos is the index of the node that the last node points to)
Output: `true`

### Python Implementation
```python
def hasCycle(head: ListNode) -> bool:
    """
    Time Complexity: O(n)
    Space Complexity: O(1)

    Floyd's Cycle-Finding Algorithm (Tortoise and Hare).
    """
    if not head:
        return False

    slow = head
    fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True

    return False
```

---

## Problem 3: Linked List Cycle II
### Problem Statement
Given the head of a linked list, return the node where the cycle begins. If there is no cycle, return null.

### Constraints
- The number of nodes in the list is in the range `[0, 10^4]`.
- `-10^5 <= Node.val <= 10^5`

### Example
Input: `head = [3,2,0,-4], pos = 1`
Output: `tail connects to node index 1`

### Python Implementation
```python
def detectCycle(head: ListNode) -> ListNode:
    """
    Time Complexity: O(n)
    Space Complexity: O(1)

    1. Detect cycle using fast and slow pointers.
    2. Reset slow to head and move both at same speed until they meet.
    """
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            # Cycle detected
            slow = head
            while slow != fast:
                slow = slow.next
                fast = fast.next
            return slow

    return None
```

---

## Problem 4: Remove Nth Node From End
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

    Use two pointers with a gap of n nodes.
    """
    dummy = ListNode(0)
    dummy.next = head
    fast = dummy
    slow = dummy

    # Move fast ahead by n + 1 steps
    for _ in range(n + 1):
        fast = fast.next

    while fast:
        slow = slow.next
        fast = fast.next

    slow.next = slow.next.next
    return dummy.next
```

---

## Problem 5: Palindrome Linked List
### Problem Statement
Given the head of a singly linked list, return true if it is a palindrome or false otherwise.

### Constraints
- The number of nodes in the list is in the range `[1, 10^5]`.
- `0 <= Node.val <= 9`

### Example
Input: `head = [1,2,2,1]`
Output: `true`

### Python Implementation
```python
def isPalindrome(head: ListNode) -> bool:
    """
    Time Complexity: O(n)
    Space Complexity: O(1)

    1. Find middle.
    2. Reverse second half.
    3. Compare first and second halves.
    """
    if not head or not head.next:
        return True

    # Find middle
    slow = fast = head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next

    # Reverse second half
    def reverse(node):
        prev = None
        while node:
            nxt = node.next
            node.next = prev
            prev = node
            node = nxt
        return prev

    second_half = reverse(slow.next)

    # Compare
    first_half = head
    while second_half:
        if first_half.val != second_half.val:
            return False
        first_half = first_half.next
        second_half = second_half.next

    return True
```
