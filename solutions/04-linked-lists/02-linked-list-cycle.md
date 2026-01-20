# Linked List Cycle

## Problem Statement

Given `head`, the head of a linked list, determine if the linked list has a cycle in it.

A cycle exists if some node can be reached again by continuously following the `next` pointer.

Return `true` if there is a cycle, `false` otherwise.

**Example:**
```
Input: head = [3, 2, 0, -4], pos = 1 (tail connects to index 1)
Output: true

Input: head = [1], pos = -1 (no cycle)
Output: false
```

## Approach

### Floyd's Cycle Detection (Tortoise and Hare)
Use two pointers:
- **Slow**: moves 1 step at a time
- **Fast**: moves 2 steps at a time

If there's a cycle, fast will eventually catch up to slow.
If no cycle, fast will reach the end.

### Why It Works
In a cycle, fast gains 1 step on slow each iteration. Eventually they meet.

## Implementation

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def has_cycle(head: ListNode) -> bool:
    """
    Detect cycle using Floyd's algorithm.

    Time: O(n)
    Space: O(1)
    """
    if not head or not head.next:
        return False

    slow = head
    fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

        if slow == fast:
            return True

    return False


def has_cycle_hashset(head: ListNode) -> bool:
    """
    Detect cycle using hash set.

    Time: O(n)
    Space: O(n)
    """
    seen = set()

    while head:
        if head in seen:
            return True
        seen.add(head)
        head = head.next

    return False


def detect_cycle(head: ListNode) -> ListNode:
    """
    Return the node where cycle begins, or None if no cycle.

    Algorithm:
    1. Find meeting point using Floyd's
    2. Move one pointer to head
    3. Move both at same speed until they meet

    Time: O(n)
    Space: O(1)
    """
    if not head or not head.next:
        return None

    slow = fast = head

    # Phase 1: Find meeting point
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            break
    else:
        return None  # No cycle

    # Phase 2: Find cycle start
    slow = head
    while slow != fast:
        slow = slow.next
        fast = fast.next

    return slow
```

## Complexity Analysis

| Method | Time | Space | Notes |
|--------|------|-------|-------|
| Floyd's | O(n) | O(1) | Optimal |
| Hash Set | O(n) | O(n) | Simpler logic |

## Why Floyd's Algorithm Works

### Cycle Detection
- Fast moves 2 steps, slow moves 1 step per iteration
- If there's a cycle, fast will eventually lap slow
- The relative speed is 1 step per iteration
- So they will definitely meet within the cycle

### Finding Cycle Start
Let:
- `F` = distance from head to cycle start
- `C` = cycle length
- When they meet, slow traveled `F + a` steps (a = distance into cycle)
- Fast traveled `F + a + nC` steps (completed some cycles)

Since fast travels twice as far:
`2(F + a) = F + a + nC`
`F + a = nC`
`F = nC - a = (n-1)C + (C - a)`

This means: distance from head to cycle start = distance from meeting point to cycle start (going around the cycle).

## Visual Walkthrough

```
List with cycle:
1 → 2 → 3 → 4 → 5
        ↑       ↓
        ← ← ← ←

Initial: slow=1, fast=1

Step 1: slow=2, fast=3
Step 2: slow=3, fast=5
Step 3: slow=4, fast=4 (in cycle, fast wrapped)

They meet at 4! Cycle detected.

Finding cycle start:
- Reset slow to head (1)
- Move both one step at a time
Step 1: slow=2, fast=5
Step 2: slow=3, fast=3

They meet at 3 → cycle starts here!
```

## Edge Cases

1. **Empty list**: No cycle
2. **Single node, no cycle**: No cycle
3. **Single node, self-loop**: Cycle exists
4. **Two nodes, cycle at head**: Works correctly
5. **Very long list**: Algorithm still O(n)
6. **Cycle of length 1** (self-loop): Works correctly

## Common Mistakes

1. **Not handling empty or single-node lists**: Check before starting
2. **Checking `fast == slow` before first move**: Start both at head, then move
3. **Wrong condition for while loop**: Need `fast and fast.next`
4. **Comparing values instead of nodes**: Must compare node references

## Variations

### Linked List Cycle II (Find Start)
Return the node where cycle begins.

### Intersection of Two Linked Lists
```python
def get_intersection_node(headA: ListNode, headB: ListNode) -> ListNode:
    """
    Find where two lists intersect.

    Idea: After traversing list A then B, both pointers
    travel same distance if there's intersection.

    Time: O(n + m)
    Space: O(1)
    """
    if not headA or not headB:
        return None

    a, b = headA, headB

    while a != b:
        a = a.next if a else headB
        b = b.next if b else headA

    return a  # Either intersection or None
```

### Find the Duplicate Number
```python
def find_duplicate(nums: list[int]) -> int:
    """
    Array where each element is in [1, n].
    One duplicate exists. Find it using cycle detection.

    Treat array as linked list: nums[i] points to nums[nums[i]]
    The duplicate creates a cycle.

    Time: O(n)
    Space: O(1)
    """
    slow = fast = nums[0]

    # Phase 1: Find meeting point
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break

    # Phase 2: Find cycle start
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]

    return slow
```

### Happy Number
```python
def is_happy(n: int) -> bool:
    """
    A happy number eventually reaches 1 through sum of squared digits.
    Use cycle detection - unhappy numbers form a cycle.

    Time: O(log n) per step, but bounded iterations
    Space: O(1)
    """
    def get_next(num):
        total = 0
        while num > 0:
            digit = num % 10
            total += digit * digit
            num //= 10
        return total

    slow = n
    fast = get_next(n)

    while fast != 1 and slow != fast:
        slow = get_next(slow)
        fast = get_next(get_next(fast))

    return fast == 1
```

## Related Problems

- **Linked List Cycle II** - Find cycle start node
- **Find the Duplicate Number** - Cycle in array
- **Happy Number** - Cycle detection in digit operations
- **Intersection of Two Linked Lists** - Similar two-pointer technique
- **Middle of Linked List** - Uses slow/fast pointers
