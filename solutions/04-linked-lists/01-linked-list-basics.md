# Solutions: Linked List Basics

## 1. Delete Node in a Linked List
**Problem Statement**: Write a function to delete a node in a singly-linked list. You will not be given access to the head of the list, instead you will be given access to the node to be deleted directly. It is guaranteed that the node to be deleted is not a tail node in the list.

### Examples & Edge Cases
- **Example 1**: `head = [4,5,1,9], node = 5` -> `[4,1,9]`
- **Example 2**: `head = [4,5,1,9], node = 1` -> `[4,5,9]`
- **Edge Case**: Deleting the first node (works fine).
- **Edge Case**: Deleting a node in the middle (works fine).
- **Note**: The problem guarantees it's not the last node.

### Optimal Python Solution
```python
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

def deleteNode(node):
    """
    Since we don't have access to the previous node, we cannot
    re-point the previous node's 'next' to skip the current node.
    Instead, we copy the data from the next node into the current node
     and skip the next node.
    """
    # Copy value from the next node to the current node
    node.val = node.next.val
    # Point the current node's next to the one after the next node
    # effectively removing the next node from the list
    node.next = node.next.next
```

### Explanation
The standard way to delete a node in a linked list is to make the `next` pointer of the *previous* node point to the *following* node. However, here we only have access to the node itself. Since we can't look back, we instead "move" the next node into our current position by copying its value and then deleting that next node.

### Complexity Analysis
- **Time Complexity**: O(1). We are only performing a value assignment and a pointer update.
- **Space Complexity**: O(1). No extra space is used regardless of the list size.

---

## 2. Remove Linked List Elements
**Problem Statement**: Given the `head` of a linked list and an integer `val`, remove all the nodes of the linked list that has `Node.val == val`, and return the new head.

### Examples & Edge Cases
- **Example 1**: `head = [1,2,6,3,4,5,6], val = 6` -> `[1,2,3,4,5]`
- **Example 2**: `head = [], val = 1` -> `[]`
- **Example 3**: `head = [7,7,7,7], val = 7` -> `[]`
- **Edge Case**: The head itself needs to be removed.
- **Edge Case**: Multiple consecutive nodes need to be removed.
- **Edge Case**: The tail needs to be removed.

### Optimal Python Solution
```python
def removeElements(head: ListNode, val: int) -> ListNode:
    # Use a dummy node to handle cases where the head needs to be deleted
    dummy = ListNode(0)
    dummy.next = head

    current = dummy
    # Traverse while there is a next node to check
    while current.next:
        if current.next.val == val:
            # Skip the next node
            current.next = current.next.next
        else:
            # Only move forward if we didn't delete the next node
            current = current.next

    return dummy.next
```

### Explanation
Using a `dummy` node that points to the head simplifies the logic significantly. It allows us to treat the `head` just like any other node, avoiding a special `if head.val == val` block. We use a single pointer `current`. If `current.next.val` is the target, we bypass it. If not, we move `current` forward.

### Complexity Analysis
- **Time Complexity**: O(n). We visit each node in the list exactly once.
- **Space Complexity**: O(1). We only use a dummy node and a pointer, which does not grow with input size.

---

## 3. Design Linked List
**Problem Statement**: Design your implementation of the linked list. You can choose to use a singly or doubly linked list.
A node in a singly linked list should have two attributes: `val` and `next`. `val` is the value of the current node, and `next` is a pointer/reference to the next node.
Implement the `MyLinkedList` class:
- `MyLinkedList()` Initializes the `MyLinkedList` object.
- `get(index)` Get the value of the `index`-th node in the linked list. If the index is invalid, return -1.
- `addAtHead(val)` Add a node of value `val` before the first element of the linked list.
- `addAtTail(val)` Append a node of value `val` as the last element of the linked list.
- `addAtIndex(index, val)` Add a node of value `val` before the `index`-th node in the linked list. If `index` equals the length of the linked list, the node will be appended to the end of the linked list. If `index` is greater than the length, the node will not be inserted.
- `deleteAtIndex(index)` Delete the `index`-th node in the linked list, if the index is valid.

### Examples & Edge Cases
- **Example**: `addAtHead(1), addAtTail(3), addAtIndex(1, 2), get(1), deleteAtIndex(1), get(1)`
- **Edge Case**: `addAtIndex` at the very beginning (index 0).
- **Edge Case**: `deleteAtIndex` at the very beginning (head).
- **Edge Case**: `addAtIndex` at the very end (tail).

### Optimal Python Solution
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

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
        self.addAtIndex(0, val)

    def addAtTail(self, val: int) -> None:
        self.addAtIndex(self.size, val)

    def addAtIndex(self, index: int, val: int) -> None:
        if index > self.size:
            return

        if index <= 0:
            self.head = ListNode(val, self.head)
        else:
            curr = self.head
            for _ in range(index - 1):
                curr = curr.next
            curr.next = ListNode(val, curr.next)

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

### Explanation
This implementation uses a singly linked list. We keep track of the `head` and the `size` of the list to make operations more efficient and handle bounds checking easily. `addAtIndex` is the core method that `addAtHead` and `addAtTail` can leverage.

### Complexity Analysis
- **Time Complexity**:
    - `get`: O(n)
    - `addAtHead`: O(1)
    - `addAtTail`: O(n) (O(1) if we kept a tail pointer)
    - `addAtIndex`: O(n)
    - `deleteAtIndex`: O(n)
- **Space Complexity**: O(n) to store the `n` elements.

---

## 4. Middle of the Linked List
**Problem Statement**: Given the `head` of a singly linked list, return the middle node of the linked list. If there are two middle nodes, return the second middle node.

### Examples & Edge Cases
- **Example 1**: `[1,2,3,4,5]` -> `[3,4,5]` (middle is 3)
- **Example 2**: `[1,2,3,4,5,6]` -> `[4,5,6]` (middle is 4)
- **Edge Case**: Single node list -> returns the node itself.
- **Edge Case**: Two node list -> returns the second node.

### Optimal Python Solution
```python
def middleNode(head: ListNode) -> ListNode:
    """
    Using the Fast and Slow pointer technique (Tortoise and Hare).
    The slow pointer moves 1 step, the fast pointer moves 2 steps.
    When fast reaches the end, slow is at the middle.
    """
    slow = head
    fast = head

    # Traverse while fast can take two steps
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    return slow
```

### Explanation
We use two pointers: `slow` and `fast`. For every step `slow` takes, `fast` takes two. This means that when `fast` reaches the end of the list (None) or the last node, `slow` will have covered exactly half the distance, landing on the middle node. This is a classic "one-pass" solution.

### Complexity Analysis
- **Time Complexity**: O(n). We traverse the list once.
- **Space Complexity**: O(1). Only two pointers are used.

---

## 5. Convert Binary Number in LL to Integer
**Problem Statement**: Given `head` which is a reference node to a singly-linked list. The value of each node in the linked list is either 0 or 1. The linked list holds the binary representation of a number. Return the decimal value of the number in the linked list.

### Examples & Edge Cases
- **Example 1**: `[1,0,1]` -> `5` (1*2^2 + 0*2^1 + 1*2^0)
- **Example 2**: `[0]` -> `0`
- **Example 3**: `[1]` -> `1`
- **Example 4**: `[1,0,0,1,0,0,1,1,1,0,0,0,0,0,0]` -> `18880`
- **Edge Case**: Large numbers within integer limits.

### Optimal Python Solution
```python
def getDecimalValue(head: ListNode) -> int:
    """
    We can build the number as we traverse.
    Each new node shifts the previous result left by 1 (multiply by 2)
    and adds the current bit.
    """
    num = 0
    curr = head
    while curr:
        # Binary shift left and OR (or just num * 2 + curr.val)
        num = (num << 1) | curr.val
        curr = curr.next
    return num
```

### Explanation
As we traverse the list from left to right, each node represents a more significant bit than the ones that follow. By multiplying our current result by 2 (or bit-shifting left) and adding the current node's value, we naturally build the decimal equivalent. For `[1, 0, 1]`:
1. `num = 0 * 2 + 1 = 1`
2. `num = 1 * 2 + 0 = 2`
3. `num = 2 * 2 + 1 = 5`

### Complexity Analysis
- **Time Complexity**: O(n). We visit each node once.
- **Space Complexity**: O(1). We only store the accumulating integer.
