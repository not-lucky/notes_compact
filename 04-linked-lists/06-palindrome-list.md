# Palindrome Linked List

> **Prerequisites:** [02-fast-slow-pointers](./02-fast-slow-pointers.md), [03-reversal-patterns](./03-reversal-patterns.md)

## Overview

Checking if a linked list is a palindrome requires comparing the first half with the reversed second half. The O(1) space solution combines fast-slow pointers (to find the middle) with in-place reversal—a beautiful synthesis of two fundamental patterns.

## Building Intuition

**Why is this problem a perfect test of fundamentals?**

This problem requires combining two techniques you've already learned:

1. Fast-slow pointers → find the middle
2. Reversal → reverse the second half
3. Comparison → walk both halves together

It's like a cooking challenge where you must combine basic techniques into a complete dish.

**The Core Strategy**:

```
Original:    [1] → [2] → [3] → [2] → [1]

Step 1: Find middle (fast-slow)
         [1] → [2] → [3] → [2] → [1]
                      ↑
                    middle

Step 2: Reverse second half
         [1] → [2] → [3] → None
         [1] → [2]              (reversed second half, starting from end)

Step 3: Compare
         [1] vs [1] ✓
         [2] vs [2] ✓
         Second half exhausted → Palindrome!
```

**Why Does the Middle Node Not Affect the Result?**

For odd-length lists, the middle element is compared with itself (via the reversal). For even-length lists, there's no true middle—both halves have equal length. Either way, the algorithm handles it correctly because:

- We only compare until the shorter half is exhausted
- The middle of an odd list ends up in the first half, not compared

**Why O(1) Space Matters**:

- Array conversion: O(n) space for storing values
- Stack approach: O(n) space for the stack
- Fast-slow + reversal: O(1) extra space (just pointers!)

**The Restoration Question**:

```python
# After checking, the list is: [1] → [2] → [3] → None  [1] ← [2]
# Should we restore it?
slow.next = reverse_list(second_half)
# Now: [1] → [2] → [3] → [2] → [1]  (original structure)
```

In interviews, always ask: "Should I preserve the original list?" Good practice is to restore it, showing attention to side effects.

**Odd vs Even Length Handling**:

```
Odd (5 elements):  [1, 2, 3, 2, 1]
  First half:  [1, 2, 3]  (middle included)
  Second half: [2, 1] reversed = [1, 2]
  Compare: [1,2,3] vs [1,2] → compare first 2 elements

Even (4 elements): [1, 2, 2, 1]
  First half:  [1, 2]
  Second half: [2, 1] reversed = [1, 2]
  Compare: [1,2] vs [1,2] → exact match
```

The fast.next and fast.next.next condition in the while loop naturally handles this split.

## When NOT to Use the O(1) Space Approach

1. **List Cannot Be Modified**: If the list is read-only or modifications cause issues (concurrent access, persistence requirements), use the array or stack approach.

2. **Need to Know Position of Mismatch**: The O(1) approach tells you true/false, not where the mismatch occurred. For debugging or partial matches, array comparison is easier.

3. **Very Short Lists**: For lists under 10 elements, the overhead of careful pointer manipulation isn't worth it. Just copy to an array.

4. **Combined with Other Operations**: If you need the original list for subsequent operations in the same problem, the restoration step adds complexity. Consider O(n) space instead.

5. **Doubly-Linked Lists**: With `.prev` pointers, you don't need reversal—just walk from both ends simultaneously.

**Common Mistake**: Forgetting the condition difference between finding middle for reversal vs. other uses. For palindrome, we want slow at the last node of the first half, not the first node of the second half.

## Interview Context

Checking if a linked list is a palindrome is a **popular interview problem** because:

1. **Combines multiple techniques**: Fast-slow pointers + reversal
2. **Space optimization**: O(1) space solution is non-trivial
3. **Edge case handling**: Odd vs even length lists
4. **Follow-up questions**: "Can you do it without modifying the list?"

This problem tests your ability to combine fundamental linked list patterns.

---

## Problem Definition

A linked list is a palindrome if it reads the same forwards and backwards.

```
Palindrome:     [1] → [2] → [3] → [2] → [1]  ✓
Not palindrome: [1] → [2] → [3] → [4] → [5]  ✗
Single node:    [1]  ✓
Empty:          None  ✓ (by convention)
```

---

## Approach 1: Array Comparison

```python
from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def is_palindrome_array(head: Optional[ListNode]) -> bool:
    """
    Convert to array and check palindrome.

    Time: O(n)
    Space: O(n)
    """
    values = []
    current = head

    while current:
        values.append(current.val)
        current = current.next

    return values == values[::-1]
```

Simple but uses O(n) extra space.

---

## Approach 2: Reverse and Compare (O(1) Space)

```python
def is_palindrome(head: Optional[ListNode]) -> bool:
    """
    Check palindrome with O(1) space.
    Strategy: Find middle, reverse second half, compare, restore.

    LeetCode 234: Palindrome Linked List

    Time: O(n)
    Space: O(1) auxiliary
    """
    if not head or not head.next:
        return True

    # Step 1: Find the middle using fast-slow pointers
    slow = fast = head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next

    # slow is now at the end of first half
    # For odd length: slow is at the middle node
    # For even length: slow is at the end of first half

    # Step 2: Reverse the second half
    second_half_start = reverse_list(slow.next)

    # Step 3: Compare first and second half
    first = head
    second = second_half_start
    result = True

    while result and second:  # Second half is shorter or equal
        if first.val != second.val:
            result = False
        else:
            first = first.next
            second = second.next

    # Step 4: Restore the list (optional but recommended)
    slow.next = reverse_list(second_half_start)

    return result


def reverse_list(head: Optional[ListNode]) -> Optional[ListNode]:
    """Reverse a linked list."""
    prev = None
    current = head

    while current:
        next_temp = current.next
        current.next = prev
        prev = current
        current = next_temp

    return prev
```

### Visual Walkthrough (Odd Length)

```
Original: [1] → [2] → [3] → [2] → [1]

Step 1: Find middle
  slow: 1 → 2 → 3 (stops here)
  fast: 1 → 3 → 5 (past end)
  slow points to 3 (middle)

Step 2: Reverse second half (after slow)
  Before: [1] → [2] → [3] → [2] → [1]
                        ↑
                      slow

  Reverse slow.next onwards:
  [1] → [2] → [3] → None
  [1] ← [2] (reversed second half, head is rightmost 1)

  Result: first half = [1] → [2] → [3] → None
          second half = [1] → [2] → None

Step 3: Compare
  first:  1 == 1 ✓
  first:  2 == 2 ✓
  second becomes None, stop

Result: True (palindrome)
```

### Visual Walkthrough (Even Length)

```
Original: [1] → [2] → [2] → [1]

Step 1: Find middle
  slow: 1 → 2 (stops here)
  fast: 1 → 3 → None (fast.next.next is None)
  slow points to first 2

Step 2: Reverse second half (after slow)
  Before: [1] → [2] → [2] → [1]
                  ↑
                slow

  Reverse slow.next onwards:
  first half = [1] → [2] → None
  second half = [1] → [2] → None

Step 3: Compare
  1 == 1 ✓
  2 == 2 ✓
  second becomes None, stop

Result: True (palindrome)
```

---

## Approach 3: Recursive

```python
def is_palindrome_recursive(head: Optional[ListNode]) -> bool:
    """
    Check palindrome recursively using implicit stack.

    Time: O(n)
    Space: O(n) - call stack
    """
    front = [head]  # Use list to maintain reference

    def check(node: Optional[ListNode]) -> bool:
        if not node:
            return True

        # Go to the end first (recursive call)
        if not check(node.next):
            return False

        # Now comparing: front pointer vs current node (from end)
        if front[0].val != node.val:
            return False

        # Move front pointer forward
        front[0] = front[0].next
        return True

    return check(head)
```

### How Recursive Approach Works

```
List: [1] → [2] → [3] → [2] → [1]

Call stack builds:
  check(1) → check(2) → check(3) → check(2) → check(1) → check(None)

Unwinding:
  check(None): return True

  check(1): front=1, node=1 → 1==1 ✓, front moves to 2

  check(2): front=2, node=2 → 2==2 ✓, front moves to 3

  check(3): front=3, node=3 → 3==3 ✓, front moves to 2

  check(2): front=2, node=2 → 2==2 ✓, front moves to 1

  check(1): front=1, node=1 → 1==1 ✓

All True → Palindrome!
```

---

## Approach 4: Stack (First Half)

```python
def is_palindrome_stack(head: Optional[ListNode]) -> bool:
    """
    Use stack to store first half, compare with second half.

    Time: O(n)
    Space: O(n/2) = O(n)
    """
    if not head or not head.next:
        return True

    # Find middle with fast-slow
    slow = fast = head
    stack = []

    while fast and fast.next:
        stack.append(slow.val)
        slow = slow.next
        fast = fast.next.next

    # If odd length, skip middle element
    if fast:  # fast is not None means odd length
        slow = slow.next

    # Compare stack (first half reversed) with second half
    while slow:
        if stack.pop() != slow.val:
            return False
        slow = slow.next

    return True
```

---

## Complexity Comparison

| Approach     | Time | Space  | Modifies List |
| ------------ | ---- | ------ | ------------- |
| Array        | O(n) | O(n)   | No            |
| Reverse half | O(n) | O(1)   | Temporarily   |
| Recursive    | O(n) | O(n)   | No            |
| Stack        | O(n) | O(n/2) | No            |

---

## Edge Cases

```python
# 1. Empty list
head = None  # → True (by convention)

# 2. Single node
head = ListNode(1)  # → True

# 3. Two nodes (same value)
head = create_linked_list([1, 1])  # → True

# 4. Two nodes (different values)
head = create_linked_list([1, 2])  # → False

# 5. Odd length palindrome
head = create_linked_list([1, 2, 1])  # → True

# 6. Even length palindrome
head = create_linked_list([1, 2, 2, 1])  # → True

# 7. Long non-palindrome
head = create_linked_list([1, 2, 3, 4, 5])  # → False

# 8. All same values
head = create_linked_list([1, 1, 1, 1, 1])  # → True
```

---

## Important: Restoring the List

If the problem requires not modifying the original list (or it's good practice to restore it):

```python
def is_palindrome_restore(head: Optional[ListNode]) -> bool:
    """Version that restores the original list."""
    if not head or not head.next:
        return True

    # Find middle
    slow = fast = head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next

    # Reverse second half
    second_half = slow.next
    reversed_second = reverse_list(second_half)

    # Compare
    p1, p2 = head, reversed_second
    result = True

    while p2:
        if p1.val != p2.val:
            result = False
            break
        p1 = p1.next
        p2 = p2.next

    # Restore: reverse back the second half
    slow.next = reverse_list(reversed_second)

    return result
```

---

## Variation: Palindrome Linked List with Odd Node

```python
def is_palindrome_allow_one_removal(head: Optional[ListNode]) -> bool:
    """
    Check if list can become palindrome by removing at most one node.

    Similar to "Valid Palindrome II" for strings.
    """
    def check_palindrome(left: Optional[ListNode], right: Optional[ListNode]) -> bool:
        # Convert to array for easier checking
        values = []
        current = left
        while current != right:
            values.append(current.val)
            current = current.next
        if right:
            values.append(right.val)
        return values == values[::-1]

    # For linked lists, this is more complex
    # Usually solved by converting to array first
    values = []
    current = head
    while current:
        values.append(current.val)
        current = current.next

    left, right = 0, len(values) - 1
    while left < right:
        if values[left] != values[right]:
            # Try skipping left or right
            skip_left = values[left+1:right+1]
            skip_right = values[left:right]
            return skip_left == skip_left[::-1] or skip_right == skip_right[::-1]
        left += 1
        right -= 1

    return True
```

---

## Interview Discussion Points

1. **Why reverse only half?** Reversing the entire list and comparing would use O(n) space for a copy.

2. **Why use fast-slow?** Finding the middle in one pass, then reversing, gives us O(1) space.

3. **Odd vs Even handling**: The key insight is that for odd-length lists, the middle element doesn't affect palindrome-ness.

4. **Restoring the list**: Good practice, and may be required if the function shouldn't have side effects.

---

## Practice Problems

| #   | Problem                | Difficulty | Key Concept             |
| --- | ---------------------- | ---------- | ----------------------- |
| 1   | Palindrome Linked List | Easy       | Fast-slow + reverse     |
| 2   | Valid Palindrome       | Easy       | Two pointers on string  |
| 3   | Valid Palindrome II    | Easy       | Allow one removal       |
| 4   | Reorder List           | Medium     | Similar split + reverse |

---

## Key Takeaways

1. **Combine fast-slow with reversal** for O(1) space palindrome check
2. **Middle finding** naturally handles odd/even lengths
3. **Only compare until second half ends** - it's shorter or equal to first half
4. **Restore the list** if modification is not allowed
5. **Recursive approach** uses O(n) stack space but is elegant
6. **Stack of first half** is intuitive but uses O(n/2) space

---

## Next: [07-dummy-node-technique.md](./07-dummy-node-technique.md)

Learn how dummy nodes simplify linked list operations by handling edge cases elegantly.
