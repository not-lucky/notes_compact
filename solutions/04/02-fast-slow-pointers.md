# Fast-Slow Pointers (Floyd's Algorithm)

## Practice Problems

### 1. Middle of the Linked List
**Difficulty:** Easy
**Key Technique:** Slow (1x) and Fast (2x) pointers

```python
def middle_node(head: ListNode) -> ListNode:
    """
    Time: O(n)
    Space: O(1)
    """
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow
```

### 2. Linked List Cycle
**Difficulty:** Easy
**Key Technique:** Fast-Slow pointers (meeting point)

```python
def has_cycle(head: ListNode) -> bool:
    """
    Time: O(n)
    Space: O(1)
    """
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False
```

### 3. Linked List Cycle II
**Difficulty:** Medium
**Key Technique:** Detect cycle + Reset slow to head

```python
def detect_cycle(head: ListNode) -> ListNode:
    """
    Find the node where the cycle begins.
    Time: O(n)
    Space: O(1)
    """
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            # Cycle found, find start
            slow = head
            while slow != fast:
                slow = slow.next
                fast = fast.next
            return slow
    return None
```

### 4. Remove Nth Node From End of List
**Difficulty:** Medium
**Key Technique:** Two pointers with fixed gap

```python
def remove_nth_from_end(head: ListNode, n: int) -> ListNode:
    """
    Time: O(n)
    Space: O(1)
    """
    dummy = ListNode(0, head)
    first = second = dummy
    # Move first ahead by n + 1 steps
    for _ in range(n + 1):
        first = first.next
    # Move both until first reaches end
    while first:
        first = first.next
        second = second.next
    # second is before the node to remove
    second.next = second.next.next
    return dummy.next
```

### 5. Palindrome Linked List
**Difficulty:** Easy
**Key Technique:** Find middle + Reverse half + Compare

```python
def is_palindrome(head: ListNode) -> bool:
    """
    Time: O(n)
    Space: O(1)
    """
    if not head or not head.next: return True
    # Find middle
    slow = fast = head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next

    # Reverse second half
    prev = None
    curr = slow.next
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt

    # Compare
    p1, p2 = head, prev
    while p2:
        if p1.val != p2.val: return False
        p1 = p1.next
        p2 = p2.next
    return True
```

### 6. Reorder List
**Difficulty:** Medium
**Key Technique:** Split + Reverse + Merge

```python
def reorder_list(head: ListNode) -> None:
    """
    Time: O(n)
    Space: O(1)
    """
    if not head: return
    # Find middle
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    # Reverse second half
    prev, curr = None, slow.next
    slow.next = None
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt

    # Merge two halves
    p1, p2 = head, prev
    while p2:
        tmp1, tmp2 = p1.next, p2.next
        p1.next = p2
        p2.next = tmp1
        p1, p2 = tmp1, tmp2
```
