# Linked List Basics

> **Prerequisites:** [01-complexity-analysis](../01-complexity-analysis/README.md)

## Interview Context

Linked lists are fundamental because:

1. **Building block**: Many advanced structures (stacks, queues, graphs) use linked lists
2. **Pointer skills**: Tests your ability to manipulate references correctly
3. **Space efficiency**: Can insert/delete without shifting elements
4. **Real-world use**: Memory allocators, undo systems, browser history

Interviewers use linked lists to assess your understanding of memory, references, and careful pointer manipulation.

---

## Core Concept: What is a Linked List?

A linked list is a linear data structure where elements are stored in **nodes**, and each node points to the next node.

```
Arrays:  [1][2][3][4][5]  ← Contiguous memory

Linked:  [1]→[2]→[3]→[4]→[5]→None  ← Scattered memory, connected by pointers
```

### Visual Representation

```
Singly Linked List:

  head
   ↓
┌─────┬──┐   ┌─────┬──┐   ┌─────┬──┐   ┌─────┬──┐
│  1  │ ─┼──→│  2  │ ─┼──→│  3  │ ─┼──→│  4  │ ─┼──→ None
└─────┴──┘   └─────┴──┘   └─────┴──┘   └─────┴──┘
  val  next    val  next    val  next    val  next


Doubly Linked List:

         head                                       tail
          ↓                                          ↓
None ←──┌─────┐   ┌─────┐   ┌─────┐   ┌─────┐──→ None
        │  1  │⇄──│  2  │⇄──│  3  │⇄──│  4  │
        └─────┘   └─────┘   └─────┘   └─────┘
```

---

## Node Definition

### Singly Linked List Node (Standard)

```python
class ListNode:
    """Standard LeetCode ListNode definition."""
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

### Doubly Linked List Node

```python
class DoublyListNode:
    """Node for doubly linked list."""
    def __init__(self, val=0, prev=None, next=None):
        self.val = val
        self.prev = prev
        self.next = next
```

---

## Basic Operations

### Creating a Linked List

```python
def create_linked_list(values: list) -> ListNode:
    """
    Create linked list from array of values.

    Time: O(n)
    Space: O(n)
    """
    if not values:
        return None

    head = ListNode(values[0])
    current = head

    for val in values[1:]:
        current.next = ListNode(val)
        current = current.next

    return head


# Usage
head = create_linked_list([1, 2, 3, 4, 5])
# Creates: 1 → 2 → 3 → 4 → 5 → None
```

### Traversal

```python
def traverse(head: ListNode) -> list:
    """
    Traverse and collect all values.

    Time: O(n)
    Space: O(n) for result, O(1) for traversal itself
    """
    result = []
    current = head

    while current:
        result.append(current.val)
        current = current.next

    return result


def print_list(head: ListNode) -> None:
    """Print linked list for debugging."""
    values = []
    current = head

    while current:
        values.append(str(current.val))
        current = current.next

    print(" → ".join(values) + " → None")
```

### Finding Length

```python
def get_length(head: ListNode) -> int:
    """
    Get the length of linked list.

    Time: O(n)
    Space: O(1)
    """
    length = 0
    current = head

    while current:
        length += 1
        current = current.next

    return length
```

### Search

```python
def search(head: ListNode, target: int) -> ListNode:
    """
    Find node with target value.

    Time: O(n)
    Space: O(1)
    """
    current = head

    while current:
        if current.val == target:
            return current
        current = current.next

    return None  # Not found
```

---

## Insertion Operations

### Insert at Head (Prepend)

```python
def insert_at_head(head: ListNode, val: int) -> ListNode:
    """
    Insert new node at the beginning.

    Time: O(1)
    Space: O(1)
    """
    new_node = ListNode(val)
    new_node.next = head
    return new_node  # New head


# Usage
head = create_linked_list([2, 3, 4])  # 2 → 3 → 4
head = insert_at_head(head, 1)         # 1 → 2 → 3 → 4
```

### Insert at Tail (Append)

```python
def insert_at_tail(head: ListNode, val: int) -> ListNode:
    """
    Insert new node at the end.

    Time: O(n) - must traverse to find tail
    Space: O(1)
    """
    new_node = ListNode(val)

    if not head:
        return new_node

    current = head
    while current.next:
        current = current.next

    current.next = new_node
    return head
```

### Insert at Position

```python
def insert_at_position(head: ListNode, val: int, position: int) -> ListNode:
    """
    Insert new node at given position (0-indexed).

    Time: O(n)
    Space: O(1)
    """
    new_node = ListNode(val)

    # Insert at head
    if position == 0:
        new_node.next = head
        return new_node

    # Traverse to position - 1
    current = head
    for _ in range(position - 1):
        if not current:
            return head  # Position out of bounds
        current = current.next

    if not current:
        return head  # Position out of bounds

    # Insert after current
    new_node.next = current.next
    current.next = new_node

    return head
```

---

## Deletion Operations

### Delete at Head

```python
def delete_at_head(head: ListNode) -> ListNode:
    """
    Delete the first node.

    Time: O(1)
    Space: O(1)
    """
    if not head:
        return None

    return head.next  # New head
```

### Delete at Tail

```python
def delete_at_tail(head: ListNode) -> ListNode:
    """
    Delete the last node.

    Time: O(n) - must find second-to-last
    Space: O(1)
    """
    if not head or not head.next:
        return None

    current = head
    while current.next.next:
        current = current.next

    current.next = None
    return head
```

### Delete by Value

```python
def delete_by_value(head: ListNode, val: int) -> ListNode:
    """
    Delete first node with given value.

    Time: O(n)
    Space: O(1)
    """
    # Handle head deletion
    if head and head.val == val:
        return head.next

    current = head
    while current and current.next:
        if current.next.val == val:
            current.next = current.next.next
            return head
        current = current.next

    return head  # Value not found
```

### Delete Node (Given Access to Node Only)

```python
def delete_node(node: ListNode) -> None:
    """
    Delete node when you only have access to that node.
    Cannot delete tail node with this approach.

    LeetCode 237: Delete Node in a Linked List

    Time: O(1)
    Space: O(1)
    """
    # Copy next node's value, then skip next node
    node.val = node.next.val
    node.next = node.next.next
```

---

## Complexity Summary

| Operation | Time Complexity | Space Complexity |
|-----------|-----------------|------------------|
| Create from array | O(n) | O(n) |
| Traverse | O(n) | O(1) |
| Search | O(n) | O(1) |
| Get length | O(n) | O(1) |
| Insert at head | O(1) | O(1) |
| Insert at tail | O(n)* | O(1) |
| Insert at position | O(n) | O(1) |
| Delete at head | O(1) | O(1) |
| Delete at tail | O(n) | O(1) |
| Delete by value | O(n) | O(1) |

*O(1) with tail pointer

---

## Common Interview Patterns

### Pattern: Two-Pass vs One-Pass

```python
# Two-pass: First count length, then traverse to position
def get_nth_from_start(head: ListNode, n: int) -> ListNode:
    current = head
    for _ in range(n):
        if not current:
            return None
        current = current.next
    return current

# One-pass: Use two pointers (covered in 02-fast-slow-pointers.md)
```

### Pattern: Previous Pointer Tracking

```python
def delete_all_occurrences(head: ListNode, val: int) -> ListNode:
    """Delete all nodes with given value."""
    # Dummy node handles edge case of deleting head
    dummy = ListNode(0)
    dummy.next = head
    prev = dummy

    current = head
    while current:
        if current.val == val:
            prev.next = current.next
        else:
            prev = current
        current = current.next

    return dummy.next
```

---

## Edge Cases

```python
# 1. Empty list
head = None
# → Handle None checks before operations

# 2. Single node
head = ListNode(1)
# → After operations, might become None

# 3. Two nodes
head = create_linked_list([1, 2])
# → Special case for many algorithms

# 4. All same values
head = create_linked_list([1, 1, 1, 1])
# → Test delete_all_occurrences type functions

# 5. Cycle (covered in 02-fast-slow-pointers.md)
# → Traversal never ends without detection
```

---

## Debugging Tips

```python
def debug_list(head: ListNode, max_nodes: int = 100) -> None:
    """
    Safe print that handles cycles.
    """
    current = head
    count = 0

    while current and count < max_nodes:
        print(f"Node {count}: val={current.val}, next={current.next}")
        current = current.next
        count += 1

    if count == max_nodes:
        print("Warning: Possible cycle or very long list")
```

---

## Practice Problems

| # | Problem | Difficulty | Key Concept |
|---|---------|------------|-------------|
| 1 | Delete Node in a Linked List | Medium | Delete without previous pointer |
| 2 | Remove Linked List Elements | Easy | Delete all occurrences |
| 3 | Design Linked List | Medium | Full implementation |
| 4 | Middle of the Linked List | Easy | Find middle (see next section) |
| 5 | Convert Binary Number in LL to Integer | Easy | Traversal with computation |

---

## Key Takeaways

1. **Nodes contain data and pointer(s)** - singly linked has `.next`, doubly has `.prev` and `.next`
2. **No random access** - must traverse from head, O(n) for access by index
3. **O(1) insertions at head** - major advantage over arrays
4. **Track previous node** for deletions (or use dummy node)
5. **Always check for None** before accessing `.next`
6. **Dummy nodes simplify edge cases** (covered in detail later)

---

## Next: [02-fast-slow-pointers.md](./02-fast-slow-pointers.md)

Learn the powerful fast-slow pointer technique for cycle detection, finding the middle, and more.
