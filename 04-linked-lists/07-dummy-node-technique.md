# Dummy Node Technique

> **Prerequisites:** [01-linked-list-basics](./01-linked-list-basics.md)

## Interview Context

The dummy node (also called sentinel node) technique is a **critical pattern** because:

1. **Eliminates edge cases**: No special handling for head modifications
2. **Cleaner code**: Fewer conditionals, less room for bugs
3. **Universal applicability**: Works for insert, delete, merge, partition, etc.
4. **Interview expectation**: Interviewers expect you to use this when appropriate

Using dummy nodes shows maturity in handling linked list problems.

---

## Core Concept

A dummy node is a fake node placed before the head. It:
- Has an arbitrary value (usually 0)
- Points to the actual head
- Simplifies operations that might modify the head

```
Without dummy:
  head → [1] → [2] → [3] → None
  (Need special handling if head changes)

With dummy:
  dummy → [1] → [2] → [3] → None
     ↑
  (dummy.next is always the real head, even after modifications)
```

---

## Pattern 1: Delete Operations

### Without Dummy Node (Complex)

```python
def remove_elements_no_dummy(head: ListNode, val: int) -> ListNode:
    """Remove all nodes with given value (without dummy)."""
    # Handle head deletions separately
    while head and head.val == val:
        head = head.next

    if not head:
        return None

    # Handle rest of list
    current = head
    while current.next:
        if current.next.val == val:
            current.next = current.next.next
        else:
            current = current.next

    return head
```

### With Dummy Node (Clean)

```python
def remove_elements(head: ListNode, val: int) -> ListNode:
    """
    Remove all nodes with given value.

    LeetCode 203: Remove Linked List Elements

    Time: O(n)
    Space: O(1)
    """
    dummy = ListNode(0)
    dummy.next = head
    current = dummy

    while current.next:
        if current.next.val == val:
            current.next = current.next.next
        else:
            current = current.next

    return dummy.next  # The real head
```

### Visual Comparison

```
Remove all 2s from: [2] → [1] → [2] → [3] → [2] → None

Without dummy:
  - First check head: 2? Yes, delete → head becomes [1]
  - Now traverse...
  (Two different code paths)

With dummy:
  dummy → [2] → [1] → [2] → [3] → [2] → None
    ↑
  current

  Step 1: current.next.val = 2, skip it
  dummy → [1] → [2] → [3] → [2] → None

  Step 2: current.next.val = 1, move current
  dummy → [1] → [2] → [3] → [2] → None
            ↑
          current

  Step 3: current.next.val = 2, skip it
  dummy → [1] → [3] → [2] → None

  (Same code path for all deletions!)
```

---

## Pattern 2: Insert Operations

```python
def insert_at_position(head: ListNode, val: int, position: int) -> ListNode:
    """
    Insert new node at given position (0-indexed).

    Time: O(n)
    Space: O(1)
    """
    dummy = ListNode(0)
    dummy.next = head
    current = dummy

    # Traverse to position
    for _ in range(position):
        if not current.next:
            break
        current = current.next

    # Insert
    new_node = ListNode(val)
    new_node.next = current.next
    current.next = new_node

    return dummy.next
```

Without dummy, inserting at position 0 would require special handling.

---

## Pattern 3: Partition List

```python
def partition(head: ListNode, x: int) -> ListNode:
    """
    Partition list so nodes < x come before nodes >= x.

    LeetCode 86: Partition List

    Time: O(n)
    Space: O(1)
    """
    # Two dummy nodes for two partitions
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

    # Connect partitions
    after.next = None  # Important: prevent cycle
    before.next = after_dummy.next

    return before_dummy.next
```

### Visual Walkthrough

```
Partition [1, 4, 3, 2, 5, 2] around x = 3

before_dummy → None
after_dummy → None

Processing:
  1 < 3: before_dummy → [1]
  4 >= 3: after_dummy → [4]
  3 >= 3: after_dummy → [4] → [3]
  2 < 3: before_dummy → [1] → [2]
  5 >= 3: after_dummy → [4] → [3] → [5]
  2 < 3: before_dummy → [1] → [2] → [2]

Connect:
  before → after:
  [1] → [2] → [2] → [4] → [3] → [5] → None

Result: [1, 2, 2, 4, 3, 5]
```

---

## Pattern 4: Merge Operations

```python
def merge_two_lists(l1: ListNode, l2: ListNode) -> ListNode:
    """
    Merge two sorted lists.

    Time: O(n + m)
    Space: O(1)
    """
    dummy = ListNode(0)
    tail = dummy

    while l1 and l2:
        if l1.val <= l2.val:
            tail.next = l1
            l1 = l1.next
        else:
            tail.next = l2
            l2 = l2.next
        tail = tail.next

    tail.next = l1 if l1 else l2

    return dummy.next
```

---

## Pattern 5: Remove Nth from End

```python
def remove_nth_from_end(head: ListNode, n: int) -> ListNode:
    """
    Remove nth node from end.

    LeetCode 19: Remove Nth Node From End of List

    Time: O(n)
    Space: O(1)
    """
    dummy = ListNode(0)
    dummy.next = head
    slow = fast = dummy

    # Move fast n+1 steps ahead
    for _ in range(n + 1):
        fast = fast.next

    # Move both until fast reaches end
    while fast:
        slow = slow.next
        fast = fast.next

    # Remove the node
    slow.next = slow.next.next

    return dummy.next
```

Without dummy: Special handling needed when removing the first node (n equals list length).

---

## Pattern 6: Remove Duplicates

### Remove All Duplicates (Keep None)

```python
def delete_duplicates_all(head: ListNode) -> ListNode:
    """
    Remove all nodes that have duplicates (keep only distinct values).

    LeetCode 82: Remove Duplicates from Sorted List II

    Time: O(n)
    Space: O(1)
    """
    dummy = ListNode(0)
    dummy.next = head
    prev = dummy

    while head:
        # Check if current is start of duplicates
        if head.next and head.val == head.next.val:
            # Skip all nodes with this value
            while head.next and head.val == head.next.val:
                head = head.next
            # Skip the last duplicate too
            prev.next = head.next
        else:
            prev = prev.next

        head = head.next

    return dummy.next
```

### Remove Duplicates (Keep One)

```python
def delete_duplicates_keep_one(head: ListNode) -> ListNode:
    """
    Remove duplicates, keeping first occurrence.

    LeetCode 83: Remove Duplicates from Sorted List

    Time: O(n)
    Space: O(1)
    """
    # No dummy needed here - head never changes
    current = head

    while current and current.next:
        if current.val == current.next.val:
            current.next = current.next.next
        else:
            current = current.next

    return head
```

---

## Pattern 7: Reverse Between

```python
def reverse_between(head: ListNode, left: int, right: int) -> ListNode:
    """
    Reverse nodes from position left to right.

    LeetCode 92: Reverse Linked List II

    Time: O(n)
    Space: O(1)
    """
    if not head or left == right:
        return head

    dummy = ListNode(0)
    dummy.next = head
    prev = dummy

    # Move to node before left
    for _ in range(left - 1):
        prev = prev.next

    # Reverse nodes from left to right
    current = prev.next
    for _ in range(right - left):
        next_node = current.next
        current.next = next_node.next
        next_node.next = prev.next
        prev.next = next_node

    return dummy.next
```

---

## When to Use Dummy Node

**Use dummy when:**
- The head might change (delete head, insert before head)
- Merging/partitioning where new head is unknown
- Any operation that modifies list structure from the beginning

**Don't need dummy when:**
- Just traversing the list
- Operations that never affect the head
- Finding/searching operations

---

## Common Patterns Summary

| Operation | Needs Dummy? | Why |
|-----------|--------------|-----|
| Remove by value | Yes | Head might be removed |
| Insert at position | Yes | Position 0 needs it |
| Merge two lists | Yes | Result head unknown |
| Partition list | Yes | Result head unknown |
| Remove nth from end | Yes | First node might be removed |
| Remove duplicates (all) | Yes | Head might be duplicate |
| Remove duplicates (keep first) | No | Head always stays |
| Reverse entire list | No | New head is predictable |
| Find middle | No | Just traversal |

---

## Edge Cases

```python
# 1. Empty list
head = None
dummy = ListNode(0)
dummy.next = head
# dummy.next is None - works fine

# 2. Single node
head = ListNode(1)
# After deletion: dummy.next might be None

# 3. Delete the only node
remove_elements(ListNode(1), 1)
# Returns None via dummy.next

# 4. All nodes deleted
remove_elements(create_linked_list([1,1,1]), 1)
# Returns None via dummy.next
```

---

## Implementation Tips

```python
# Standard dummy node setup
dummy = ListNode(0)  # or ListNode(-1), value doesn't matter
dummy.next = head

# Work with the list...

# Return the real head
return dummy.next


# Two dummies for partitioning
dummy1 = ListNode(0)
dummy2 = ListNode(0)
# ... separate nodes into two lists ...
# Connect if needed
dummy1_tail.next = dummy2.next
return dummy1.next
```

---

## Practice Problems

| # | Problem | Difficulty | Key Concept |
|---|---------|------------|-------------|
| 1 | Remove Linked List Elements | Easy | Basic dummy usage |
| 2 | Remove Nth Node From End | Medium | Dummy + two pointers |
| 3 | Partition List | Medium | Two dummy nodes |
| 4 | Remove Duplicates II | Medium | Dummy for head deletion |
| 5 | Merge Two Sorted Lists | Easy | Dummy for unknown head |
| 6 | Reverse Linked List II | Medium | Dummy for position operations |

---

## Key Takeaways

1. **Dummy node prevents special cases** for head operations
2. **Always return `dummy.next`** - that's the real head after modifications
3. **Use multiple dummies** when building multiple lists (partition)
4. **Dummy value is arbitrary** - use 0 or -1 or any value
5. **Recognize patterns**: If head might change, use dummy
6. **Cleaner code = fewer bugs** - dummy eliminates edge case branches

---

## Next: [08-copy-with-random.md](./08-copy-with-random.md)

Learn how to deep copy a linked list with random pointers - a challenging but common interview problem.
