# Palindrome Linked List

## Practice Problems

### 1. Palindrome Linked List
**Difficulty:** Easy
**Key Technique:** Fast-Slow pointers + Reverse second half

```python
def is_palindrome(head: ListNode) -> bool:
    """
    Check if a linked list is a palindrome.
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
    res = True
    while p2:
        if p1.val != p2.val:
            res = False
            break
        p1, p2 = p1.next, p2.next

    # Restore (optional)
    # curr, prev = prev, None
    # while curr:
    #     nxt = curr.next
    #     curr.next = prev
    #     prev = curr
    #     curr = nxt
    # slow.next = prev

    return res
```

### 2. Palindrome Linked List (Recursive)
**Difficulty:** Easy
**Key Technique:** Implicit stack comparison

```python
def is_palindrome_recursive(head: ListNode) -> bool:
    """
    Time: O(n)
    Space: O(n)
    """
    left = head
    def check(right):
        nonlocal left
        if not right: return True
        res = check(right.next)
        if not res: return False
        if left.val != right.val: return False
        left = left.next
        return True
    return check(head)
```

### 3. Reorder List
**Difficulty:** Medium
**Key Technique:** Split + Reverse + Interleave

```python
def reorder_list(head: ListNode) -> None:
    """
    Time: O(n)
    Space: O(1)
    """
    if not head or not head.next: return
    # Find middle
    slow = fast = head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next

    # Reverse second half
    prev, curr = None, slow.next
    slow.next = None
    while curr:
        nxt = curr.next
        curr.next = prev
        prev, curr = curr, nxt

    # Merge
    p1, p2 = head, prev
    while p2:
        tmp1, tmp2 = p1.next, p2.next
        p1.next = p2
        p2.next = tmp1
        p1, p2 = tmp1, tmp2
```
