# Solution: Linked List Basics Practice Problems

## Problem 1: Delete Node in a Linked List
### Problem Statement
Write a function to delete a node in a singly-linked list. You will not be given access to the head of the list, instead you will be given access to the node to be deleted directly. It is guaranteed that the node to be deleted is not a tail node in the list.

### Constraints
- The number of the nodes in the given list is in the range `[2, 1000]`.
- `-1000 <= Node.val <= 1000`
- The value of each node in the list is unique.
- The node to be deleted is in the list and is not a tail node.

### Example
Input: `head = [4,5,1,9], node = 5`
Output: `[4,1,9]`

### Python Implementation
```python
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

def deleteNode(node: ListNode) -> None:
    """
    Time Complexity: O(1)
    Space Complexity: O(1)

    Since we don't have access to the previous node, we copy the value
    from the next node into the current node, then delete the next node.
    """
    node.val = node.next.val
    node.next = node.next.next
```

---

## Problem 2: Remove Linked List Elements
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

## Problem 3: Design Linked List
### Problem Statement
Design your implementation of the linked list. You can choose to use a singly or doubly linked list.
A node in a singly linked list should have two attributes: `val` and `next`. `val` is the value of the current node, and `next` is a pointer/reference to the next node.
If you want to use the doubly linked list, you will need one more attribute `prev` to indicate the previous node in the linked list. Assume all nodes in the linked list are 0-indexed.

Implement the `MyLinkedList` class:
- `MyLinkedList()` Initializes the `MyLinkedList` object.
- `get(index)` Get the value of the `index`th node in the linked list. If the index is invalid, return -1.
- `addAtHead(val)` Add a node of value `val` before the first element of the linked list. After the insertion, the new node will be the first node of the linked list.
- `addAtTail(val)` Append a node of value `val` as the last element of the linked list.
- `addAtIndex(index, val)` Add a node of value `val` before the `index`th node in the linked list. If `index` equals the length of the linked list, the node will be appended to the end of the linked list. If `index` is greater than the length, the node will not be inserted.
- `deleteAtIndex(index)` Delete the `index`th node in the linked list, if the index is valid.

### Constraints
- `0 <= index, val <= 1000`
- Please do not use the built-in LinkedList library.
- At most 2000 calls will be made to `get`, `addAtHead`, `addAtTail`, `addAtIndex`, and `deleteAtIndex`.

### Example
Input: `["MyLinkedList", "addAtHead", "addAtTail", "addAtIndex", "get", "deleteAtIndex", "get"]`, `[[], [1], [3], [1, 2], [1], [1], [1]]`
Output: `[null, null, null, null, 2, null, 3]`

### Python Implementation
```python
class MyLinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def get(self, index: int) -> int:
        if index < 0 or index >= self.size:
            return -1
        curr = self.head
        for _ in range(index):
            curr = curr.next
        return curr.val

    def addAtHead(self, val: int) -> None:
        new_node = ListNode(val)
        new_node.next = self.head
        self.head = new_node
        self.size += 1

    def addAtTail(self, val: int) -> None:
        if self.size == 0:
            self.addAtHead(val)
            return
        curr = self.head
        while curr.next:
            curr = curr.next
        curr.next = ListNode(val)
        self.size += 1

    def addAtIndex(self, index: int, val: int) -> None:
        if index < 0 or index > self.size:
            return
        if index == 0:
            self.addAtHead(val)
            return
        curr = self.head
        for _ in range(index - 1):
            curr = curr.next
        new_node = ListNode(val)
        new_node.next = curr.next
        curr.next = new_node
        self.size += 1

    def deleteAtIndex(self, index: int) -> None:
        if index < 0 or index >= self.size:
            return
        if index == 0:
            self.head = self.head.next
        else:
            curr = self.head
            for _ in range(index - 1):
                curr = curr.next
            curr.next = curr.next.next
        self.size -= 1
```

---

## Problem 4: Middle of the Linked List
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

## Problem 5: Convert Binary Number in LL to Integer
### Problem Statement
Given head which is a reference node to a singly-linked list. The value of each node in the linked list is either 0 or 1. The linked list holds the binary representation of a number.
Return the decimal value of the number in the linked list.

### Constraints
- The Linked List is not empty.
- Number of nodes will not exceed 30.
- Each node's value is either 0 or 1.

### Example
Input: `head = [1,0,1]`
Output: `5`

### Python Implementation
```python
def getDecimalValue(head: ListNode) -> int:
    """
    Time Complexity: O(n)
    Space Complexity: O(1)

    Traverse the list and build the number using bitwise operations or multiplication.
    """
    num = 0
    curr = head
    while curr:
        num = (num << 1) | curr.val
        curr = curr.next
    return num
```
