# Reversal Patterns

## Practice Problems

### 1. Reverse Linked List
**Difficulty:** Easy
**Key Technique:** Three pointers (prev, curr, nxt)

```python
def reverse_list(head: ListNode) -> ListNode:
    """
    Time: O(n)
    Space: O(1)
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

### 2. Reverse Linked List II
**Difficulty:** Medium
**Key Technique:** Position to left, then reverse sublist

```python
def reverse_between(head: ListNode, left: int, right: int) -> ListNode:
    """
    Time: O(n)
    Space: O(1)
    """
    if not head or left == right: return head
    dummy = ListNode(0, head)
    prev = dummy
    for _ in range(left - 1):
        prev = prev.next

    curr = prev.next
    for _ in range(right - left):
        nxt = curr.next
        curr.next = nxt.next
        nxt.next = prev.next
        prev.next = nxt
    return dummy.next
```

### 3. Swap Nodes in Pairs
**Difficulty:** Medium
**Key Technique:** Dummy node + pairwise swap

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
        # Move forward
        prev = p1
    return dummy.next
```

### 4. Reverse Nodes in k-Group
**Difficulty:** Hard
**Key Technique:** Check k nodes + reverse sublist

```python
def reverse_k_group(head: ListNode, k: int) -> ListNode:
    """
    Time: O(n)
    Space: O(1)
    """
    def reverse(h, t):
        prev, curr = t.next, h
        while prev != t:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        return t, h

    dummy = ListNode(0, head)
    pre = dummy
    while head:
        tail = pre
        for _ in range(k):
            tail = tail.next
            if not tail: return dummy.next
        nxt = tail.next
        head, tail = reverse(head, tail)
        pre.next = head
        tail.next = nxt
        pre = tail
        head = nxt
    return dummy.next
```

### 5. Rotate List
**Difficulty:** Medium
**Key Technique:** Circle the list + find new tail

```python
def rotate_right(head: ListNode, k: int) -> ListNode:
    """
    Time: O(n)
    Space: O(1)
    """
    if not head or not head.next or k == 0: return head
    # Length and tail
    curr, n = head, 1
    while curr.next:
        curr = curr.next
        n += 1
    # Connect tail to head
    curr.next = head
    # New tail at n - (k % n) - 1
    k %= n
    for _ in range(n - k):
        curr = curr.next
    # Break
    res = curr.next
    curr.next = None
    return res
```
