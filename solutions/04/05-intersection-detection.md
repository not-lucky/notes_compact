# Intersection Detection

## Practice Problems

### 1. Intersection of Two Linked Lists
**Difficulty:** Easy
**Key Technique:** Two pointers (Distance Equalization)

```python
def get_intersection_node(headA: ListNode, headB: ListNode) -> ListNode:
    """
    Find the node where two singly linked lists intersect.
    Time: O(N + M)
    Space: O(1)
    """
    if not headA or not headB: return None
    p1, p2 = headA, headB
    while p1 != p2:
        p1 = p1.next if p1 else headB
        p2 = p2.next if p2 else headA
    return p1
```

### 2. Check if Two Lists Intersect
**Difficulty:** Easy
**Key Technique:** Compare tails

```python
def do_intersect(headA: ListNode, headB: ListNode) -> bool:
    """
    Check if two lists share any common node.
    Time: O(N + M)
    Space: O(1)
    """
    if not headA or not headB: return False
    # Find tail of A
    t1 = headA
    while t1.next: t1 = t1.next
    # Find tail of B
    t2 = headB
    while t2.next: t2 = t2.next
    # If they intersect, they share the same tail
    return t1 is t2
```

### 3. Intersection Point (Length Alignment)
**Difficulty:** Easy
**Key Technique:** Align starting positions

```python
def get_intersection_node_align(headA: ListNode, headB: ListNode) -> ListNode:
    """
    Time: O(N + M)
    Space: O(1)
    """
    def get_len(h):
        l = 0
        while h:
            l += 1
            h = h.next
        return l

    l1, l2 = get_len(headA), get_len(headB)
    p1, p2 = headA, headB
    # Advance longer list
    if l1 > l2:
        for _ in range(l1 - l2): p1 = p1.next
    else:
        for _ in range(l2 - l1): p2 = p2.next
    # Walk together
    while p1 != p2:
        p1, p2 = p1.next, p2.next
    return p1
```
