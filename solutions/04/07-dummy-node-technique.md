# Dummy Node Technique

## Practice Problems

### 1. Remove Linked List Elements
**Difficulty:** Easy
**Key Technique:** Dummy node absorbs head deletion

```python
def remove_elements(head: ListNode, val: int) -> ListNode:
    """
    Time: O(n)
    Space: O(1)
    """
    dummy = ListNode(0, head)
    curr = dummy
    while curr.next:
        if curr.next.val == val:
            curr.next = curr.next.next
        else:
            curr = curr.next
    return dummy.next
```

### 2. Partition List
**Difficulty:** Medium
**Key Technique:** Two dummy nodes (before and after)

```python
def partition(head: ListNode, x: int) -> ListNode:
    """
    Time: O(n)
    Space: O(1)
    """
    before_dummy = ListNode(0)
    after_dummy = ListNode(0)
    before, after = before_dummy, after_dummy

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

### 3. Remove Duplicates from Sorted List II
**Difficulty:** Medium
**Key Technique:** Dummy + Skip all duplicates

```python
def delete_duplicates(head: ListNode) -> ListNode:
    """
    Remove all nodes that have duplicate numbers.
    Time: O(n)
    Space: O(1)
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

### 4. Swap Nodes in Pairs
**Difficulty:** Medium
**Key Technique:** Dummy + prev pointer tracking

```python
def swap_pairs(head: ListNode) -> ListNode:
    """
    Time: O(n)
    Space: O(1)
    """
    dummy = ListNode(0, head)
    prev = dummy
    while prev.next and prev.next.next:
        p1 = prev.next
        p2 = p1.next
        # Swap
        p1.next = p2.next
        p2.next = p1
        prev.next = p2
        # Move
        prev = p1
    return dummy.next
```
