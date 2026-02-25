# Reversal Patterns

> **Prerequisites:** [01-linked-list-basics](./01-linked-list-basics.md)

## Overview

Linked list reversal is the process of making each node point to its predecessor instead of its successor. It's a fundamental building block for palindrome checks, reordering lists, and many other operations. Mastering the iterative three-pointer technique is essential.

## Building Intuition

**Why is reversal so important?**

Reversal is like learning multiplication tables—it's used everywhere as a building block:

- Palindrome check? Reverse half and compare.
- Add two numbers (most significant first)? Reverse, add, reverse back.
- Reorder list (L0→Ln→L1→Ln-1...)? Split, reverse second half, interleave.

**The Core Insight: You Only Need Three Pointers**

At any moment during reversal, you need to track:

1. **prev**: The already-reversed portion (or None initially)
2. **current**: The node you're currently reversing
3. **next_temp**: Saved reference to the rest of the list

Why save `next_temp`? Because once you point `current.next = prev`, you've lost your only link to the rest of the list! It's like walking across a bridge while dismantling it behind you—you need to know where the next plank is before removing the current one.

**Visual Mental Model**:

```
Step N:
None ← [A] ← [B]       [C] → [D] → [E]
              prev      curr   next_temp (curr.next)

1. Reverse pointer: `curr.next = prev`
None ← [A] ← [B] ← [C]       [D] → [E]
              prev  curr      next_temp

2. Move forward: `prev = curr`, `curr = next_temp`
None ← [A] ← [B] ← [C]       [D] → [E]
                    prev      curr   next_temp (new curr.next)

Key: At each step, `curr` points BACK to `prev`, then everyone moves forward one spot.
```

**Why Does Recursive Reversal Use O(n) Space?**

The call stack holds n frames (one per node). Each frame remembers "where to return" and the local variables. Iterative reversal uses O(1) space because we explicitly manage the pointers ourselves.

**Partial Reversal Insight**: When reversing positions left to right, the trick is:

1. Find the node BEFORE position left (this anchors the reversed segment)
2. The node originally at position left becomes the TAIL of the reversed segment
3. Keep moving nodes from "after current" to "right after anchor"

## When NOT to Use Reversal

1. **When Order Must Be Preserved**: If the problem requires maintaining original order (like filtering by condition), reversal is overkill.

2. **When a Stack/Recursion is Clearer**: Sometimes pushing to a stack and popping achieves the same "reverse processing" with clearer code, especially for value-based operations (not structural changes).

3. **When Random Access Exists**: For arrays, `arr[::-1]` or index arithmetic is simpler than explicit reversal.

4. **When You Need the Original List**: Reversal modifies the list in-place. If you need both versions, you must copy first (O(n) space anyway).

5. **For Doubly-Linked Lists**: Just traverse backwards using `.prev` instead of reversing.

**Common Mistake**: Reversing when you only need to traverse backwards. For "print in reverse order," use recursion or a stack—don't actually reverse the structure.

## Interview Context

Linked list reversal is a **fundamental interview skill** because:

1. **Frequently tested**: Appears directly or as a subproblem in many questions
2. **Tests pointer skills**: Requires careful manipulation of next pointers
3. **Multiple approaches**: Iterative vs recursive, each with trade-offs
4. **Building block**: Used in palindrome check, reorder list, reverse k-group, etc.

Being able to reverse a linked list confidently and quickly is essential.

---

## Pattern 1: Reverse Entire List (Iterative)

```python
from typing import Optional

def reverse_list(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Reverse entire linked list iteratively.

    LeetCode 206: Reverse Linked List

    Time: O(n)
    Space: O(1)
    """
    prev = None
    current = head

    while current:
        next_temp = current.next  # Save next
        current.next = prev       # Reverse pointer
        prev = current            # Move prev forward
        current = next_temp       # Move current forward

    return prev  # prev is new head
```

### Visual Walkthrough

```
Initial: 1 → 2 → 3 → 4 → None
         ↑
       head
       current
prev = None

Step 1: Save next (2)
        Reverse 1's pointer: 1 → None
        Move: prev=1, current=2

        None ← 1   2 → 3 → 4 → None
               ↑   ↑
             prev current

Step 2: Save next (3)
        Reverse 2's pointer: 2 → 1
        Move: prev=2, current=3

        None ← 1 ← 2   3 → 4 → None
                   ↑   ↑
                 prev current

Step 3: Save next (4)
        Reverse 3's pointer: 3 → 2
        Move: prev=3, current=4

        None ← 1 ← 2 ← 3   4 → None
                       ↑   ↑
                     prev current

Step 4: Save next (None)
        Reverse 4's pointer: 4 → 3
        Move: prev=4, current=None

        None ← 1 ← 2 ← 3 ← 4
                           ↑
                         prev (new head)

Result: 4 → 3 → 2 → 1 → None
```

---

## Pattern 2: Reverse Entire List (Recursive)

```python
def reverse_list_recursive(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Reverse entire linked list recursively.

    Time: O(n)
    Space: O(n) - call stack
    """
    # Base case: empty or single node
    if not head or not head.next:
        return head

    # Reverse rest of list
    new_head = reverse_list_recursive(head.next)

    # Reverse the connection
    head.next.next = head
    head.next = None

    return new_head
```

### Understanding Recursive Reversal

```
reverse([1] → [2] → [3] → None)

Call stack builds up:
  reverse(1) calls reverse(2)
    reverse(2) calls reverse(3)
      reverse(3) returns 3 (base case: single node)

    Back in reverse(2):
      new_head = 3
      2.next.next = 2  →  3.next = 2  →  3 → 2
      2.next = None    →  3 → 2 → None
      return 3

  Back in reverse(1):
    new_head = 3
    1.next.next = 1  →  2.next = 1  →  3 → 2 → 1
    1.next = None    →  3 → 2 → 1 → None
    return 3

Result: 3 → 2 → 1 → None
```

---

## Pattern 3: Reverse Between Positions (Reverse Sublist)

```python
def reverse_between(head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
    """
    Reverse nodes from position left to right (1-indexed).

    LeetCode 92: Reverse Linked List II

    Time: O(n)
    Space: O(1)
    """
    if not head or left == right:
        return head

    dummy = ListNode(0)
    dummy.next = head
    prev = dummy

    # Step 1: Move prev to node before left
    for _ in range(left - 1):
        prev = prev.next

    # Step 2: Reverse from left to right
    current = prev.next
    for _ in range(right - left):
        next_node = current.next
        current.next = next_node.next
        next_node.next = prev.next
        prev.next = next_node

    return dummy.next
```

### Visual Walkthrough (left=2, right=4)

```
Initial: 1 → 2 → 3 → 4 → 5
             ↑       ↑
           left    right

After positioning prev before left:
         ↓
dummy → [1] → [2] → [3] → [4] → [5]
        prev  curr

Iteration 1 (move 3 to front of sublist):
dummy → [1] → [3] → [2] → [4] → [5]
        prev        curr

Iteration 2 (move 4 to front of sublist):
dummy → [1] → [4] → [3] → [2] → [5]
        prev              curr

Result: 1 → 4 → 3 → 2 → 5
```

---

## Pattern 4: Reverse in K-Groups

```python
def reverse_k_group(head: Optional[ListNode], k: int) -> Optional[ListNode]:
    """
    Reverse nodes in k-group. Leftover nodes remain as is.

    LeetCode 25: Reverse Nodes in k-Group

    Time: O(n)
    Space: O(1)
    """
    # Check if we have k nodes
    def get_kth_node(start: ListNode, k: int) -> ListNode:
        while start and k > 1:
            start = start.next
            k -= 1
        return start

    dummy = ListNode(0)
    dummy.next = head
    prev_group_end = dummy

    while True:
        kth = get_kth_node(prev_group_end.next, k)

        if not kth:
            break  # Less than k nodes remaining

        next_group_start = kth.next

        # Reverse k nodes
        prev, current = kth.next, prev_group_end.next
        while current != next_group_start:
            next_temp = current.next
            current.next = prev
            prev = current
            current = next_temp

        # Connect with previous and next groups
        temp = prev_group_end.next
        prev_group_end.next = kth
        prev_group_end = temp

    return dummy.next
```

### Visual Walkthrough (k=3)

```
Initial: [1] → [2] → [3] → [4] → [5] → [6] → [7] → [8]

Group 1 (nodes 1-3):
  Before: [1] → [2] → [3] → [4] → ...
  After:  [3] → [2] → [1] → [4] → ...

Group 2 (nodes 4-6):
  Before: [3] → [2] → [1] → [4] → [5] → [6] → [7] → [8]
  After:  [3] → [2] → [1] → [6] → [5] → [4] → [7] → [8]

Remaining (nodes 7-8): Less than k, keep as is

Result: [3] → [2] → [1] → [6] → [5] → [4] → [7] → [8]
```

---

## Pattern 5: Reverse Alternating K-Groups

```python
def reverse_alternate_k_group(head: Optional[ListNode], k: int) -> Optional[ListNode]:
    """
    Reverse nodes in alternating k-groups.
    Reverse first k, skip next k, reverse next k, etc.

    Time: O(n)
    Space: O(1)
    """
    def count_nodes(start: ListNode, k: int) -> bool:
        """Check if at least k nodes exist."""
        count = 0
        while start and count < k:
            start = start.next
            count += 1
        return count == k

    dummy = ListNode(0)
    dummy.next = head
    prev = dummy
    should_reverse = True

    while head:
        if not count_nodes(head, k):
            break

        if should_reverse:
            # Reverse k nodes
            tail = head
            current = head
            prev_node = None

            for _ in range(k):
                next_temp = current.next
                current.next = prev_node
                prev_node = current
                current = next_temp

            prev.next = prev_node
            tail.next = current
            prev = tail
            head = current
        else:
            # Skip k nodes
            for _ in range(k):
                prev = head
                head = head.next

        should_reverse = not should_reverse

    return dummy.next
```

---

## Pattern 6: Reverse Pairs (Swap Nodes in Pairs)

```python
def swap_pairs(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Swap every two adjacent nodes.

    LeetCode 24: Swap Nodes in Pairs

    Time: O(n)
    Space: O(1)
    """
    dummy = ListNode(0)
    dummy.next = head
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

### Visual Walkthrough

```
Initial: dummy → [1] → [2] → [3] → [4]
                  ↑     ↑
               first  second

After swap 1:
         dummy → [2] → [1] → [3] → [4]
                        ↑     ↑     ↑
                      prev  first second

After swap 2:
         dummy → [2] → [1] → [4] → [3]
                              ↑
                            prev

Result: [2] → [1] → [4] → [3]
```

---

## Recursive Swap Pairs

```python
def swap_pairs_recursive(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Swap every two adjacent nodes recursively.

    Time: O(n)
    Space: O(n) - call stack
    """
    if not head or not head.next:
        return head

    first = head
    second = head.next

    # Swap and connect to recursive result
    first.next = swap_pairs_recursive(second.next)
    second.next = first

    return second
```

---

## Complexity Summary

| Pattern                    | Time | Space |
| -------------------------- | ---- | ----- |
| Reverse entire (iterative) | O(n) | O(1)  |
| Reverse entire (recursive) | O(n) | O(n)  |
| Reverse between            | O(n) | O(1)  |
| Reverse k-group            | O(n) | O(1)  |
| Swap pairs                 | O(n) | O(1)  |

---

## Common Variations

### Rotate List

While not strictly a reversal problem, rotating a list is often grouped with reversal patterns because it involves reconnecting the list. Note that this problem does *not* require reversing pointers, but rather breaking the list and forming a circle, then breaking it again at the right spot.

```python
def rotate_right(head: Optional[ListNode], k: int) -> Optional[ListNode]:
    """
    Rotate list to the right by k places.

    LeetCode 61: Rotate List

    Time: O(n)
    Space: O(1)
    """
    if not head or not head.next or k == 0:
        return head

    # Find length and tail
    length = 1
    tail = head
    while tail.next:
        tail = tail.next
        length += 1

    # Handle k > length
    k = k % length
    if k == 0:
        return head

    # Make circular
    tail.next = head

    # Find new tail (length - k steps from head)
    # The new tail will be at position length - k - 1 (0-indexed)
    steps_to_new_tail = length - k
    new_tail = head
    for _ in range(steps_to_new_tail - 1):
        new_tail = new_tail.next

    # Break the circle
    new_head = new_tail.next
    new_tail.next = None

    return new_head
```

---

## Edge Cases

```python
# 1. Empty list
head = None  # Return None

# 2. Single node
head = ListNode(1)  # Return as is for most operations

# 3. Two nodes
head = create_linked_list([1, 2])
# Swap pairs: [2, 1]
# Reverse: [2, 1]

# 4. k larger than list length
# reverse_k_group([1, 2], k=3) → [1, 2] (no change)

# 5. left = right in reverse_between
# No change needed
```

---

## Interview Tips

1. **Draw it out**: Always visualize with boxes and arrows
2. **Use dummy node**: Simplifies edge cases for head changes
3. **Track three pointers**: prev, current, next_temp
4. **Check boundaries**: left/right bounds, k groups
5. **Test edge cases**: Empty, single node, exact k nodes

---

## Practice Problems

| #   | Problem                  | Difficulty | Key Concept               |
| --- | ------------------------ | ---------- | ------------------------- |
| 1   | Reverse Linked List      | Easy       | Basic reversal            |
| 2   | Reverse Linked List II   | Medium     | Reverse between positions |
| 3   | Swap Nodes in Pairs      | Medium     | Reverse pairs             |
| 4   | Reverse Nodes in k-Group | Hard       | Reverse k nodes at a time |
| 5   | Rotate List              | Medium     | Rotation via reversal     |
| 6   | Reorder List             | Medium     | Split + reverse + merge   |
| 7   | Add Two Numbers II       | Medium     | Reverse, add, reverse     |

---

## Key Takeaways

1. **Three-pointer technique**: prev, current, next_temp is the core pattern
2. **Iterative is O(1) space**, recursive is O(n) due to call stack
3. **Dummy node prevents edge cases** when head might change
4. **Reverse sublist**: Position pointers correctly before reversing
5. **K-group**: Check if k nodes exist before reversing
6. **Practice drawing**: Visual understanding prevents bugs

---

## Next: [04-merge-lists.md](./04-merge-lists.md)

Learn how to merge sorted linked lists efficiently.
