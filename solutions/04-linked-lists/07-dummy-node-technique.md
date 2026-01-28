# Solutions: Dummy Node Technique

## 1. Remove Linked List Elements

**Problem Statement**: Given the `head` of a linked list and an integer `val`, remove all the nodes of the linked list that has `Node.val == val`, and return the new head.

### Examples & Edge Cases

- **Example 1**: `head = [1,2,6,3,4,5,6], val = 6` -> `[1,2,3,4,5]`
- **Example 2**: `head = [], val = 1` -> `[]`
- **Example 3**: `head = [7,7,7,7], val = 7` -> `[]`
- **Edge Case**: Head itself matches `val`.
- **Edge Case**: All nodes match `val`.

### Optimal Python Solution

```python
def removeElements(head: ListNode, val: int) -> ListNode:
    """
    Using a dummy node allows us to handle head deletion
    identically to any other node deletion.
    """
    dummy = ListNode(0)
    dummy.next = head
    curr = dummy

    while curr.next:
        if curr.next.val == val:
            # Skip the next node
            curr.next = curr.next.next
        else:
            # Only advance if we didn't delete the next node
            curr = curr.next

    return dummy.next
```

### Explanation

By introducing a `dummy` node that points to the `head`, we ensure that every node we might want to delete (including the original head) has a `prev` node. This allows for a single, unified `while` loop without special logic for the head.

### Complexity Analysis

- **Time Complexity**: O(n). We visit each node once.
- **Space Complexity**: O(1). Only a dummy node and a pointer are used.

---

## 2. Remove Nth Node From End

**Problem Statement**: Given the `head` of a linked list, remove the `n`-th node from the end of the list and return its head.

### Examples & Edge Cases

- **Example**: `head = [1,2,3,4,5], n = 2` -> `[1,2,3,5]`
- **Edge Case**: Removing the head (`n = length`).

### Optimal Python Solution

```python
def removeNthFromEnd(head: ListNode, n: int) -> ListNode:
    """
    Dummy node handles the edge case where the head is removed.
    """
    dummy = ListNode(0, head)
    fast = slow = dummy

    # Move fast n+1 steps ahead to create a gap
    for _ in range(n + 1):
        fast = fast.next

    # Move both until fast hits the end
    while fast:
        fast = fast.next
        slow = slow.next

    # slow is now at the node BEFORE the target
    slow.next = slow.next.next

    return dummy.next
```

### Explanation

The `dummy` node is essential here for cases like `[1], n=1`. Without the dummy, `slow` wouldn't have a node _before_ the head to start from, making head removal difficult.

### Complexity Analysis

- **Time Complexity**: O(n).
- **Space Complexity**: O(1).

---

## 3. Partition List

**Problem Statement**: Given the `head` of a linked list and a value `x`, partition it such that all nodes less than `x` come before nodes greater than or equal to `x`. You should preserve the original relative order of the nodes in each of the two partitions.

### Examples & Edge Cases

- **Example 1**: `head = [1,4,3,2,5,2], x = 3` -> `[1,2,2,4,3,5]`
- **Example 2**: `head = [2,1], x = 2` -> `[1,2]`
- **Edge Case**: All nodes are smaller than `x`.
- **Edge Case**: All nodes are larger than `x`.

### Optimal Python Solution

```python
def partition(head: ListNode, x: int) -> ListNode:
    """
    Use two separate lists (with dummies) to collect nodes,
    then stitch them together.
    """
    before_dummy = ListNode(0)
    after_dummy = ListNode(0)

    before = before_dummy
    after = after_dummy

    curr = head
    while curr:
        if curr.val < x:
            before.next = curr
            before = before.next
        else:
            after.next = curr
            after = after.next
        curr = curr.next

    # Important: Terminate the 'after' list to avoid cycles
    after.next = None
    # Stitch 'before' to the start of 'after'
    before.next = after_dummy.next

    return before_dummy.next
```

### Explanation

We maintain two separate chains: one for nodes smaller than `x` and one for the rest. Dummy nodes make it trivial to start these chains. After a single pass through the original list, we connect the end of the `before` chain to the beginning of the `after` chain.

### Complexity Analysis

- **Time Complexity**: O(n). One pass through the list.
- **Space Complexity**: O(1). We are reusing existing nodes, just using two dummy placeholders.

---

## 4. Remove Duplicates II

**Problem Statement**: Given the `head` of a sorted linked list, delete all nodes that have duplicate numbers, leaving only distinct numbers from the original list. Return the linked list sorted as well.

### Examples & Edge Cases

- **Example 1**: `head = [1,2,3,3,4,4,5]` -> `[1,2,5]`
- **Example 2**: `head = [1,1,1,2,3]` -> `[2,3]`
- **Edge Case**: The head itself is a duplicate and needs to be removed.
- **Edge Case**: The entire list consists of duplicates.

### Optimal Python Solution

```python
def deleteDuplicates(head: ListNode) -> ListNode:
    """
    Dummy node is used because the head itself might be a duplicate
    and need to be removed.
    """
    dummy = ListNode(0, head)
    prev = dummy

    while head:
        # If it's a beginning of duplicates range
        if head.next and head.val == head.next.val:
            # Skip all nodes with the same value
            while head.next and head.val == head.next.val:
                head = head.next
            # Point prev to the first node after the duplicates range
            prev.next = head.next
        else:
            # No duplicate, move prev forward
            prev = prev.next

        # Move head forward
        head = head.next

    return dummy.next
```

### Explanation

We use `prev` to keep track of the last known "distinct" node. When we encounter a sequence of duplicates, we skip the entire sequence and link `prev.next` to the node following the sequence. If no duplicate is found, we just move `prev` forward.

### Complexity Analysis

- **Time Complexity**: O(n). Each node is visited at most twice.
- **Space Complexity**: O(1).

---

## 5. Merge Two Sorted Lists

**Problem Statement**: Merge two sorted linked lists.

### Optimal Python Solution

```python
def mergeTwoLists(l1: ListNode, l2: ListNode) -> ListNode:
    dummy = curr = ListNode(0)
    while l1 and l2:
        if l1.val < l2.val:
            curr.next, l1 = l1, l1.next
        else:
            curr.next, l2 = l2, l2.next
        curr = curr.next
    curr.next = l1 or l2
    return dummy.next
```

### Explanation

The dummy node serves as the starting point of the merged list, allowing us to append nodes from `l1` or `l2` without checking if the result list is empty.

### Complexity Analysis

- **Time Complexity**: O(n + m).
- **Space Complexity**: O(1).

---

## 6. Reverse Linked List II

**Problem Statement**: Reverse a sublist from position `left` to `right`.

### Optimal Python Solution

```python
def reverseBetween(head: ListNode, left: int, right: int) -> ListNode:
    dummy = ListNode(0, head)
    prev = dummy
    for _ in range(left - 1):
        prev = prev.next

    curr = prev.next
    for _ in range(right - left):
        temp = curr.next
        curr.next = temp.next
        temp.next = prev.next
        prev.next = temp

    return dummy.next
```

### Explanation

The dummy node handles the case where `left = 1` (the head is reversed). It provides a stable `prev` pointer to anchor the reversal.

### Complexity Analysis

- **Time Complexity**: O(n).
- **Space Complexity**: O(1).
