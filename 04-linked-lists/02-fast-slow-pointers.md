# Fast-Slow Pointers (Floyd's Algorithm)

> **Prerequisites:** [01-linked-list-basics](./01-linked-list-basics.md)

## Overview

The fast-slow pointer technique (tortoise and hare) uses two pointers moving at different speeds to solve linked list problems in O(1) space. It's the key to cycle detection, finding midpoints, and locating elements relative to the end—all without knowing the list length upfront.

## Building Intuition

**Why do two pointers at different speeds work?**

1. **The Racing Analogy**: Imagine two runners on a circular track. If runner A is twice as fast as runner B, they will meet again after A completes one full lap more than B. This is the foundation of cycle detection—if there's a loop, fast will "lap" slow.

2. **The Midpoint Discovery**: If fast moves 2 steps per iteration and slow moves 1 step, when fast reaches the end (n steps), slow is at n/2. No need to count the length first!

3. **The Mathematical Invariant**: At any point, fast has traveled exactly 2× the distance of slow. This ratio is maintained throughout, which is why:
   - For midpoint: fast at end → slow at middle
   - For nth from end: create a gap of n, then move together

**Why O(1) Space?**: We only use two pointers, no matter the list size. Alternatives like "convert to array then analyze" use O(n) space.

**The Cycle Detection Proof** (simplified):

```
If there's a cycle of length C, and slow enters the cycle:
- Both pointers are now on the cycle
- Their distance decreases by 1 each step (fast gains 1 step on slow)
- After at most C steps, distance becomes 0 → they meet

The key insight: once both are on the cycle, the "gap" shrinks every iteration.
```

**Mental Model for Cycle Start**: After detecting a cycle, why does resetting one pointer to head work? Because the distance from head to cycle start equals the distance from meeting point to cycle start (plus some complete cycles). It's like two people walking around a track—if they start at the right positions and walk at the same speed, they'll meet at the cycle entrance.

## When NOT to Use Fast-Slow Pointers

This pattern isn't always the answer:

1. **Need to Preserve Positions**: Fast-slow for palindrome check reverses half the list. If you can't modify the list, use a stack or recursion instead (O(n) space).

2. **Need All Elements, Not Just Relative Positions**: If you need to process every element (not just find a special one), a simple traversal is clearer.

3. **Array Problems with Random Access**: For arrays, using indices is usually cleaner. Fast-slow shines when you can't use indices (linked lists) or want O(1) space (Floyd's cycle in arrays).

4. **When a Hash Set is Simpler**: Cycle detection can also use a hash set—O(n) space but conceptually simpler. Choose based on constraints.

5. **When Length is Readily Available**: If you already know the list length, direct calculation is cleaner than fast-slow for midpoint/nth-from-end.

**Red Flags**:

- "Return all positions of X" → Simple traversal
- "Memory doesn't matter" → Consider hash-based approaches for clarity
- "Need to backtrack" → Doubly-linked list or stack

## Interview Context

The fast-slow pointer technique (also called the "tortoise and hare" algorithm) is one of the **most important patterns** in linked list problems because:

1. **O(1) space**: Solves problems without extra data structures
2. **One-pass solutions**: Often achieves optimal time complexity
3. **Versatility**: Cycle detection, finding middle, nth from end, and more
4. **Interview favorite**: Appears in ~30% of linked list interview questions

Master this pattern and you'll solve many problems elegantly.

---

## Core Concept

Use two pointers moving at different speeds:

- **Slow pointer**: Moves 1 step at a time
- **Fast pointer**: Moves 2 steps at a time

```
Initial:    fast
            slow
             ↓
            [1] → [2] → [3] → [4] → [5] → None

Step 1:          slow
                        fast
             ↓           ↓
            [1] → [2] → [3] → [4] → [5] → None

Step 2:                slow
                                    fast
                  ↓                   ↓
            [1] → [2] → [3] → [4] → [5] → None

Step 3:                      slow         fast
                       ↓                   ↓
            [1] → [2] → [3] → [4] → [5] → None
                                          (fast reaches end)
```

When fast reaches the end, slow is at the middle!

---

## Pattern 1: Find Middle of Linked List

```python
from typing import Optional

def find_middle(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Find the middle node of linked list.
    For even-length lists, returns the second middle node.

    LeetCode 876: Middle of the Linked List

    Time: O(n)
    Space: O(1)
    """
    slow = fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    return slow  # slow is at middle


# Examples:
# [1, 2, 3, 4, 5] → returns node with value 3
# [1, 2, 3, 4, 5, 6] → returns node with value 4 (second middle)
```

### Why Does This Work?

```
When fast travels 2n steps, slow travels n steps.
When fast reaches the end (position n), slow is at position n/2 (middle).

For odd length (n=5):
  fast: 0 → 2 → 4 → (stop, no next.next)
  slow: 0 → 1 → 2 (middle)

For even length (n=6):
  fast: 0 → 2 → 4 → (stop at None)
  slow: 0 → 1 → 2 → 3 (second middle)
```

### Variation: First Middle for Even-Length Lists

```python
def find_first_middle(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    For even-length lists, returns the first middle node.
    [1, 2, 3, 4] → returns node 2 (not 3)
    """
    slow = fast = head

    # Slightly different condition
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next

    return slow
```

---

## Pattern 2: Detect Cycle (Floyd's Cycle Detection)

```python
def has_cycle(head: Optional[ListNode]) -> bool:
    """
    Detect if linked list has a cycle.

    LeetCode 141: Linked List Cycle

    Time: O(n)
    Space: O(1)
    """
    if not head or not head.next:
        return False

    slow = head
    fast = head.next  # Start fast one step ahead

    while slow != fast:
        if not fast or not fast.next:
            return False  # Reached end, no cycle
        slow = slow.next
        fast = fast.next.next

    return True  # slow met fast, cycle exists
```

### Alternative Implementation (Both Start at Head)

```python
def has_cycle_v2(head: Optional[ListNode]) -> bool:
    """Alternative: both start at head."""
    slow = fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True

    return False
```

### Visual Example

```
List with cycle:
        ┌─────────────────────┐
        ↓                     │
[1] → [2] → [3] → [4] → [5] ─┘

slow: 1 → 2 → 3 → 4 → 5 → 3 → 4
fast: 1 → 3 → 5 → 4 → 3 → 5 → 4 → ...

They meet at some point inside the cycle!
```

---

## Pattern 3: Find Cycle Start

```python
def detect_cycle_start(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Find the node where the cycle begins.
    Returns None if no cycle.

    LeetCode 142: Linked List Cycle II

    Time: O(n)
    Space: O(1)
    """
    if not head or not head.next:
        return None

    # Phase 1: Detect if cycle exists
    slow = fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            break
    else:
        return None  # No cycle

    # Phase 2: Find cycle start
    # Reset slow to head, keep fast at meeting point
    slow = head
    while slow != fast:
        slow = slow.next
        fast = fast.next  # Both move at same speed now

    return slow  # Meeting point is cycle start
```

### Mathematical Proof (Interview Talking Point)

```
Let:
- F = distance from head to cycle start
- C = cycle length
- a = distance from cycle start to meeting point

When they meet:
- slow traveled: F + a
- fast traveled: F + a + n*C (some number of complete cycles)

Since fast travels 2× slow's speed:
  2(F + a) = F + a + n*C
  F + a = n*C
  F = n*C - a

This means: distance from head to cycle start (F) equals
            distance from meeting point to cycle start (C - a)

So if we reset one pointer to head and move both at same speed,
they'll meet at the cycle start!
```

---

## Pattern 4: Remove Nth Node From End

```python
def remove_nth_from_end(head: Optional[ListNode], n: int) -> Optional[ListNode]:
    """
    Remove the nth node from the end of the list.

    LeetCode 19: Remove Nth Node From End of List

    Time: O(n) - one pass
    Space: O(1)
    """
    dummy = ListNode(0)
    dummy.next = head
    slow = fast = dummy

    # Move fast n+1 steps ahead to maintain a gap of n between slow and fast
    for _ in range(n + 1):
        if not fast:
            return head # Handle edge case where n is larger than list length
        fast = fast.next

    # Move both until fast reaches the end
    while fast:
        slow = slow.next
        fast = fast.next

    # slow is now just before the node to remove
    if slow.next:
        slow.next = slow.next.next

    return dummy.next
```

### Visual Walkthrough

```
Remove 2nd from end: [1, 2, 3, 4, 5]

Initial (after moving fast n+1=3 steps):
dummy → [1] → [2] → [3] → [4] → [5] → None
  ↑                   ↑
 slow                fast

After moving both until fast is None:
dummy → [1] → [2] → [3] → [4] → [5] → None
                      ↑                  ↑
                    slow               fast

slow.next = [4] is the node to remove!
```

---

## Pattern 5: Find List Length and Nth From End

```python
def get_nth_from_end(head: Optional[ListNode], n: int) -> Optional[ListNode]:
    """
    Get the nth node from the end (1-indexed).
    Returns None if n is out of bounds.

    Time: O(n)
    Space: O(1)
    """
    slow = fast = head

    # Move fast n steps ahead
    for _ in range(n):
        if not fast:
            return None  # n is larger than list length
        fast = fast.next

    # Move both until fast reaches end
    while fast:
        slow = slow.next
        fast = fast.next

    return slow  # slow is at nth from end
```

---

## Pattern 6: Check if Linked List is Palindrome

```python
def is_palindrome(head: Optional[ListNode]) -> bool:
    """
    Check if linked list is a palindrome.
    Combines fast-slow with reversal.

    LeetCode 234: Palindrome Linked List

    Time: O(n)
    Space: O(1)
    """
    if not head or not head.next:
        return True

    # Step 1: Find middle using fast-slow
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    # Step 2: Reverse second half
    second_half = reverse_list(slow)

    # Step 3: Compare first and second half
    first = head
    second = second_half

    result = True
    # Only need to check until second reaches the end
    while result and second:
        if first.val != second.val:
            result = False
        first = first.next
        second = second.next

    # Step 4: Restore the list (optional but highly recommended)
    # Re-reverse the second half back to its original state
    reverse_list(second_half)

    return result


def reverse_list(head: Optional[ListNode]) -> Optional[ListNode]:
    """Helper: reverse linked list."""
    prev = None
    current = head

    while current:
        next_temp = current.next
        current.next = prev
        prev = current
        current = next_temp

    return prev
```

---

## Complexity Summary

| Problem             | Time | Space |
| ------------------- | ---- | ----- |
| Find middle         | O(n) | O(1)  |
| Detect cycle        | O(n) | O(1)  |
| Find cycle start    | O(n) | O(1)  |
| Remove nth from end | O(n) | O(1)  |
| Palindrome check    | O(n) | O(1)  |

---

## Common Variations

### Split List in Half

```python
def split_list(head: Optional[ListNode]) -> tuple[Optional[ListNode], Optional[ListNode]]:
    """Split list into two halves."""
    if not head or not head.next:
        return head, None

    slow = head
    fast = head.next

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    second = slow.next
    slow.next = None  # Cut the connection

    return head, second
```

### Find Length of Cycle

```python
def cycle_length(head: Optional[ListNode]) -> int:
    """
    Find the length of the cycle.
    Returns 0 if no cycle.
    """
    slow = fast = head

    # Find meeting point
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            break
    else:
        return 0  # No cycle

    # Count cycle length
    length = 1
    current = slow.next
    while current != slow:
        length += 1
        current = current.next

    return length
```

---

## Edge Cases

```python
# 1. Empty list
head = None  # fast-slow won't enter while loop

# 2. Single node
head = ListNode(1)
# middle = itself
# no cycle possible (unless points to itself)

# 3. Two nodes
head = create_linked_list([1, 2])
# middle = second node
# need to handle carefully in some problems

# 4. Cycle at head (entire list is cycle)
node1 = ListNode(1)
node2 = ListNode(2)
node1.next = node2
node2.next = node1  # Full cycle
```

---

## Practice Problems

| #   | Problem                   | Difficulty | Key Concept                |
| --- | ------------------------- | ---------- | -------------------------- |
| 1   | Middle of the Linked List | Easy       | Basic fast-slow            |
| 2   | Linked List Cycle         | Easy       | Cycle detection            |
| 3   | Linked List Cycle II      | Medium     | Find cycle start           |
| 4   | Remove Nth Node From End  | Medium     | Two-pointer gap            |
| 5   | Palindrome Linked List    | Easy       | Fast-slow + reverse        |
| 6   | Reorder List              | Medium     | Split + reverse + merge    |
| 7   | Happy Number              | Easy       | Cycle detection on numbers |

---

## Key Takeaways

1. **Fast moves 2x, slow moves 1x** - fundamental principle
2. **When fast reaches end, slow is at middle** - exactly half the steps
3. **If they meet, there's a cycle** - no other way to meet in a finite list
4. **Cycle start = reset slow to head, move both at 1x** - mathematical property
5. **Gap technique for nth from end** - move fast n steps first
6. **O(1) space** - major advantage over using extra data structures

---

## Next: [03-reversal-patterns.md](./03-reversal-patterns.md)

Learn the essential linked list reversal patterns used in countless interview problems.
