# Intersection Detection

> **Prerequisites:** [01-linked-list-basics](./01-linked-list-basics.md)

## Overview

Finding the intersection point of two linked lists determines where two separate chains merge into one shared tail. The elegant two-pointer technique solves this in O(n+m) time with O(1) space by having each pointer traverse both lists, equalizing their total travel distances.

## Building Intuition

**Why does the two-pointer switch technique work?**

This is one of the most elegant algorithms in computer science. The magic lies in distance equalization.

**The Distance Equalization Insight**:
```
List A: ─────•─────────────•─────────• (length a + shared)
             ↑              intersection
List B: ──•──•─────────────•─────────• (length b + shared)
          ↑                 intersection
```

If A and B have different lengths, a pointer starting at A will reach the intersection at a different time than one starting at B. But here's the trick:

- Pointer A travels: a + shared + b (traverse A, then B)
- Pointer B travels: b + shared + a (traverse B, then A)

Both travel the same total distance: a + b + shared. They arrive at the intersection simultaneously!

**The Mental Model**:
Imagine two people walking toward each other on different roads that merge:
- Alice walks road A (3 miles), reaches the merge, continues on road B (5 miles)
- Bob walks road B (5 miles), reaches the merge, continues on road A (3 miles)

Both walk exactly 8 miles. If there's a meeting point, they arrive together. If not, they both reach the end at the same time (both become None).

**Why This Beats Hash Set**:
- Hash set: O(n) space to store all nodes from one list
- Two pointers: O(1) space, same time complexity

**The Length-Alignment Alternative**:
```
1. Count length of A (len_a), length of B (len_b)
2. Advance the longer list's pointer by |len_a - len_b|
3. Now both are equidistant from intersection (if exists)
4. Walk together until they meet or both hit None
```

This is more intuitive but requires two passes over each list (count + walk) vs the single-pass elegance of the switch technique.

**Critical Point: Reference vs Value**
```python
# WRONG: Comparing values
if node_a.val == node_b.val:  # Different nodes can have same value!

# RIGHT: Comparing identity
if node_a is node_b:  # Same object in memory
```

Intersection means the same physical node in memory, not just equal values.

## When NOT to Use Intersection Detection

1. **Looking for Value Equality**: If you want to find where two lists have the same values (not the same nodes), this algorithm doesn't apply.

2. **Lists That Diverge After "Meeting"**: Standard intersection assumes once lists meet, they never diverge. For DAG-like structures, use different approaches.

3. **Need All Common Nodes**: This finds the first intersection point. If you need all nodes that appear in both lists (by value), use a hash set.

4. **Circular Lists**: If either list is circular, the algorithm may loop infinitely. Detect cycles first.

5. **When Modifying Lists is OK**: If you can modify the lists, simpler approaches exist (mark visited nodes, use negative values as flags, etc.).

**Common Mistake**: Forgetting to handle the no-intersection case. The two-pointer technique naturally returns None when lists don't intersect—both pointers reach None at the same time.

## Interview Context

Finding the intersection point of two linked lists is a **classic interview question** because:

1. **Multiple solutions**: Tests ability to compare approaches
2. **Elegant O(1) space solution**: Two-pointer technique shines here
3. **Mathematical insight**: Length difference approach demonstrates analytical thinking
4. **Real-world analogy**: Two paths merging into one (file systems, roads)

This problem appears frequently at top tech companies.

---

## Problem Definition

Given two singly linked lists, find the node where they intersect.

```
List A:      a1 → a2
                    ↘
                     c1 → c2 → c3 → None
                    ↗
List B: b1 → b2 → b3

Intersection at: c1
```

Important notes:
- The intersection is by **reference** (same node object), not by value
- After intersection, both lists share the same tail
- If no intersection exists, return None

---

## Approach 1: Hash Set

```python
def get_intersection_node_hashset(headA: ListNode, headB: ListNode) -> ListNode:
    """
    Find intersection using hash set.

    Time: O(n + m)
    Space: O(n) or O(m) - store one list's nodes
    """
    # Store all nodes from list A
    seen = set()
    current = headA

    while current:
        seen.add(current)  # Store node reference, not value
        current = current.next

    # Find first node in B that's in the set
    current = headB
    while current:
        if current in seen:
            return current
        current = current.next

    return None
```

---

## Approach 2: Two Pointers (Optimal)

```python
def get_intersection_node(headA: ListNode, headB: ListNode) -> ListNode:
    """
    Find intersection using two pointers.
    The elegant O(1) space solution.

    LeetCode 160: Intersection of Two Linked Lists

    Time: O(n + m)
    Space: O(1)
    """
    if not headA or not headB:
        return None

    pA = headA
    pB = headB

    # If they intersect, they'll meet.
    # If not, both will reach None at the same time.
    while pA != pB:
        # When reaching end, switch to the other list's head
        pA = pA.next if pA else headB
        pB = pB.next if pB else headA

    return pA  # Either intersection node or None
```

### Why This Works (The Magic)

```
List A: a1 → a2 → c1 → c2 → c3 → None
List B: b1 → b2 → b3 → c1 → c2 → c3 → None

Length of A = 2 + 3 = 5 (a-part + c-part)
Length of B = 3 + 3 = 6 (b-part + c-part)

Pointer A travels: a1 → a2 → c1 → c2 → c3 → None → b1 → b2 → b3 → c1
                   (A's nodes)                        (B's unique nodes)

Pointer B travels: b1 → b2 → b3 → c1 → c2 → c3 → None → a1 → a2 → c1
                   (B's nodes)                        (A's unique nodes)

Both pointers travel: len(A) + len(B) - len(common) steps to meet at c1

Distance A travels before meeting: 5 + 3 = 8
Distance B travels before meeting: 6 + 2 = 8

They meet at the intersection!
```

### Visual Trace

```
Step 0:  pA = a1, pB = b1
Step 1:  pA = a2, pB = b2
Step 2:  pA = c1, pB = b3
Step 3:  pA = c2, pB = c1  ← Different positions
Step 4:  pA = c3, pB = c2
Step 5:  pA = None, pB = c3
Step 6:  pA = b1, pB = None  ← A switches to B, B switches to A
Step 7:  pA = b2, pB = a1
Step 8:  pA = b3, pB = a2
Step 9:  pA = c1, pB = c1  ← They meet!

Return c1
```

---

## Approach 3: Length Difference

```python
def get_intersection_node_length(headA: ListNode, headB: ListNode) -> ListNode:
    """
    Find intersection by aligning list lengths.

    Time: O(n + m)
    Space: O(1)
    """
    def get_length(head: ListNode) -> int:
        length = 0
        while head:
            length += 1
            head = head.next
        return length

    lenA = get_length(headA)
    lenB = get_length(headB)

    # Align starting positions
    pA, pB = headA, headB

    if lenA > lenB:
        for _ in range(lenA - lenB):
            pA = pA.next
    else:
        for _ in range(lenB - lenA):
            pB = pB.next

    # Now both pointers are same distance from intersection
    while pA != pB:
        pA = pA.next
        pB = pB.next

    return pA
```

### Visual Example

```
List A:      [a1] → [a2] → [c1] → [c2] → [c3]     (len = 5)
List B: [b1] → [b2] → [b3] → [c1] → [c2] → [c3]  (len = 6)

Difference: 6 - 5 = 1

Advance pB by 1:
pA starts at: a1
pB starts at: b2  (skipped b1)

Now both are 5 steps from end:
  pA: a1 → a2 → c1 → c2 → c3
  pB: b2 → b3 → c1 → c2 → c3

They'll meet at c1!
```

---

## Edge Cases

```python
# 1. No intersection (lists are completely separate)
A: [1] → [2] → [3] → None
B: [4] → [5] → None
# Return None

# 2. One or both lists are empty
A: None
B: [1] → [2]
# Return None

# 3. Intersection at head
A: [1] → [2] → [3]
B: same list (B = A)
# Return head (node with value 1)

# 4. Lists of very different lengths
A: [1] → [2] → [3] → [4] → [5] → [6] → [7] → [8] → [9] → [10]
B: [100] → [8] → [9] → [10]  (intersects at 8)
# Algorithm handles this via length alignment

# 5. Intersection at last node
A: [1] → [2] → [3] → [4]
B: [5] → [6] → [4]  (only last node shared)
# Return node 4
```

---

## Testing for Intersection

```python
def create_intersecting_lists(a_vals: list, b_vals: list, common_vals: list):
    """
    Helper to create two intersecting lists for testing.
    """
    # Create common part
    common_head = None
    for val in reversed(common_vals):
        node = ListNode(val)
        node.next = common_head
        common_head = node

    # Create list A
    a_head = common_head
    for val in reversed(a_vals):
        node = ListNode(val)
        node.next = a_head
        a_head = node

    # Create list B (need to find the common_head again)
    b_head = common_head
    for val in reversed(b_vals):
        node = ListNode(val)
        node.next = b_head
        b_head = node

    return a_head, b_head, common_head


# Usage
a, b, intersection = create_intersecting_lists([1, 2], [3, 4, 5], [6, 7, 8])
# a: 1 → 2 → 6 → 7 → 8
# b: 3 → 4 → 5 → 6 → 7 → 8
# intersection: node with value 6
```

---

## Complexity Comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Hash Set | O(n + m) | O(n) | Simple but uses extra space |
| Two Pointers | O(n + m) | O(1) | Elegant, optimal |
| Length Difference | O(n + m) | O(1) | Two passes but intuitive |

---

## Related Variations

### Find If Two Lists Intersect (Just Boolean)

```python
def lists_intersect(headA: ListNode, headB: ListNode) -> bool:
    """Check if two lists share any common node."""
    if not headA or not headB:
        return False

    # Find tail of A
    tailA = headA
    while tailA.next:
        tailA = tailA.next

    # Find tail of B
    tailB = headB
    while tailB.next:
        tailB = tailB.next

    # If they intersect, they share the same tail
    return tailA is tailB
```

### Find All Intersection Points (If Multiple Possible)

In the standard problem, once lists intersect, they never diverge. But if the question allows divergence (like in a DAG), you'd need a different approach using sets.

---

## Common Mistakes

1. **Comparing values instead of references**
   ```python
   # WRONG
   if nodeA.val == nodeB.val:  # Values can be equal without intersection

   # RIGHT
   if nodeA is nodeB:  # Same object in memory
   ```

2. **Infinite loop with different lengths**
   ```python
   # WRONG: This never terminates if lists don't intersect
   while pA and pB:
       if pA == pB:
           return pA
       pA = pA.next if pA.next else headB
       pB = pB.next if pB.next else headA

   # RIGHT: Use the switch-to-None technique
   while pA != pB:
       pA = pA.next if pA else headB
       pB = pB.next if pB else headA
   ```

3. **Forgetting to handle non-intersecting case**
   - The two-pointer approach naturally handles this: both reach None together

---

## Interview Tips

1. **Clarify the problem**: Intersection by reference, not value
2. **Mention trade-offs**: Hash set is simpler, two-pointer is optimal
3. **Explain the math**: Why two pointers meet at intersection
4. **Handle edge cases**: Empty lists, no intersection, same list

---

## Practice Problems

| # | Problem | Difficulty | Key Concept |
|---|---------|------------|-------------|
| 1 | Intersection of Two Linked Lists | Easy | Two-pointer technique |
| 2 | Find the Duplicate Number | Medium | Related: cycle detection in array |

---

## Key Takeaways

1. **Two-pointer switch technique** is elegant O(1) space solution
2. **Length alignment** is intuitive alternative
3. **Hash set** works but uses O(n) space
4. **Compare references**, not values
5. **After intersection, lists share same tail** - useful for quick check
6. **Both pointers travel same total distance** to meet at intersection

---

## Next: [06-palindrome-list.md](./06-palindrome-list.md)

Learn how to check if a linked list is a palindrome using fast-slow pointers and reversal.
