# Reverse Linked List

## Problem Statement

Given the head of a singly linked list, reverse the list, and return the reversed list.

**Example:**
```
Input: head = [1, 2, 3, 4, 5]
Output: [5, 4, 3, 2, 1]

Input: head = [1, 2]
Output: [2, 1]

Input: head = []
Output: []
```

## Approach

### Iterative (Optimal)
Use three pointers: `prev`, `curr`, `next`
1. Save next node
2. Reverse current node's pointer
3. Move prev and curr forward
4. Repeat until end

### Recursive
Recursively reverse the rest of the list, then fix the pointers.

## Implementation

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def reverse_list(head: ListNode) -> ListNode:
    """
    Reverse linked list iteratively.

    Time: O(n) - single pass
    Space: O(1) - only pointer variables
    """
    prev = None
    curr = head

    while curr:
        next_node = curr.next  # Save next
        curr.next = prev       # Reverse pointer
        prev = curr            # Move prev forward
        curr = next_node       # Move curr forward

    return prev  # New head


def reverse_list_recursive(head: ListNode) -> ListNode:
    """
    Reverse linked list recursively.

    Time: O(n)
    Space: O(n) - recursion stack
    """
    # Base case: empty or single node
    if not head or not head.next:
        return head

    # Reverse the rest
    new_head = reverse_list_recursive(head.next)

    # Fix the pointers
    head.next.next = head  # Make next node point back
    head.next = None       # Remove original forward pointer

    return new_head


def reverse_between(head: ListNode, left: int, right: int) -> ListNode:
    """
    Reverse nodes from position left to right (1-indexed).

    Example: [1,2,3,4,5], left=2, right=4 → [1,4,3,2,5]
    """
    if not head or left == right:
        return head

    dummy = ListNode(0, head)
    prev = dummy

    # Move to node before left position
    for _ in range(left - 1):
        prev = prev.next

    # Reverse from left to right
    curr = prev.next
    for _ in range(right - left):
        next_node = curr.next
        curr.next = next_node.next
        next_node.next = prev.next
        prev.next = next_node

    return dummy.next
```

## Complexity Analysis

| Method | Time | Space | Notes |
|--------|------|-------|-------|
| Iterative | O(n) | O(1) | Optimal |
| Recursive | O(n) | O(n) | Stack space |

## Visual Walkthrough

### Iterative

```
Initial: 1 → 2 → 3 → 4 → 5 → None
         prev=None, curr=1

Step 1: prev=None, curr=1
        next_node = 2
        1.next = None (was 2)
        prev = 1, curr = 2
        Result: None ← 1   2 → 3 → 4 → 5

Step 2: prev=1, curr=2
        next_node = 3
        2.next = 1
        prev = 2, curr = 3
        Result: None ← 1 ← 2   3 → 4 → 5

Step 3: prev=2, curr=3
        next_node = 4
        3.next = 2
        prev = 3, curr = 4
        Result: None ← 1 ← 2 ← 3   4 → 5

Step 4: prev=3, curr=4
        next_node = 5
        4.next = 3
        prev = 4, curr = 5
        Result: None ← 1 ← 2 ← 3 ← 4   5

Step 5: prev=4, curr=5
        next_node = None
        5.next = 4
        prev = 5, curr = None
        Result: None ← 1 ← 2 ← 3 ← 4 ← 5

Return prev (5) as new head
```

### Recursive

```
reverse_list(1) calls reverse_list(2)
reverse_list(2) calls reverse_list(3)
reverse_list(3) calls reverse_list(4)
reverse_list(4) calls reverse_list(5)
reverse_list(5) returns 5 (base case)

Unwinding:
- At node 4: 5.next = 4, 4.next = None → 5 → 4
- At node 3: 4.next = 3, 3.next = None → 5 → 4 → 3
- At node 2: 3.next = 2, 2.next = None → 5 → 4 → 3 → 2
- At node 1: 2.next = 1, 1.next = None → 5 → 4 → 3 → 2 → 1
```

## Edge Cases

1. **Empty list**: Return None
2. **Single node**: Return the node (already reversed)
3. **Two nodes**: Swap pointers correctly
4. **Cycle in list**: Algorithm would infinite loop (undefined behavior)

## Common Mistakes

1. **Losing reference to next node**: Must save `curr.next` before reversing
2. **Wrong return value**: Return `prev`, not `curr` (curr is None)
3. **Not handling empty list**: Check `if not head`
4. **Forgetting to set tail's next to None**: In recursive, `head.next = None`

## Variations

### Reverse Linked List II (Partial Reversal)
Reverse nodes from position m to n.

### Reverse Nodes in k-Group
```python
def reverse_k_group(head: ListNode, k: int) -> ListNode:
    """
    Reverse every k nodes.

    Time: O(n)
    Space: O(1)
    """
    def reverse(start, end):
        """Reverse from start to node before end."""
        prev = end
        while start != end:
            next_node = start.next
            start.next = prev
            prev = start
            start = next_node
        return prev

    def get_kth(node, k):
        """Get kth node from current."""
        while node and k > 0:
            node = node.next
            k -= 1
        return node

    dummy = ListNode(0, head)
    group_prev = dummy

    while True:
        kth = get_kth(group_prev, k)
        if not kth:
            break

        group_next = kth.next
        # Reverse group
        prev, curr = kth.next, group_prev.next
        while curr != group_next:
            next_node = curr.next
            curr.next = prev
            prev = curr
            curr = next_node

        tmp = group_prev.next
        group_prev.next = kth
        group_prev = tmp

    return dummy.next
```

### Swap Nodes in Pairs
```python
def swap_pairs(head: ListNode) -> ListNode:
    """
    Swap every two adjacent nodes.

    Time: O(n)
    Space: O(1)
    """
    dummy = ListNode(0, head)
    prev = dummy

    while prev.next and prev.next.next:
        first = prev.next
        second = prev.next.next

        # Swap
        first.next = second.next
        second.next = first
        prev.next = second

        prev = first

    return dummy.next
```

### Palindrome Linked List
```python
def is_palindrome(head: ListNode) -> bool:
    """
    Check if linked list is palindrome.
    Uses reverse + slow-fast pointer.

    Time: O(n)
    Space: O(1)
    """
    if not head or not head.next:
        return True

    # Find middle (slow will be at middle)
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    # Reverse second half
    prev = None
    while slow:
        next_node = slow.next
        slow.next = prev
        prev = slow
        slow = next_node

    # Compare halves
    left, right = head, prev
    while right:
        if left.val != right.val:
            return False
        left = left.next
        right = right.next

    return True
```

## Related Problems

- **Reverse Linked List II** - Reverse portion of list
- **Reverse Nodes in k-Group** - Reverse every k nodes
- **Swap Nodes in Pairs** - Special case of k=2
- **Palindrome Linked List** - Uses reversal as subroutine
- **Reorder List** - Combines reverse and merge
