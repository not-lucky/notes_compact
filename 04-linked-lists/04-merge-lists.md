# Merge Operations

> **Prerequisites:** [01-linked-list-basics](./01-linked-list-basics.md)

## Interview Context

Merge operations on linked lists are **essential interview topics** because:

1. **Classic algorithm**: Merge two sorted lists is a fundamental technique
2. **Building block**: Used in merge sort for linked lists
3. **Scalability**: "Merge K sorted" tests efficiency thinking
4. **Real-world relevance**: Combining sorted data streams

Mastering merge operations demonstrates solid understanding of pointer manipulation.

---

## Pattern 1: Merge Two Sorted Lists

```python
def merge_two_lists(l1: ListNode, l2: ListNode) -> ListNode:
    """
    Merge two sorted linked lists into one sorted list.

    LeetCode 21: Merge Two Sorted Lists

    Time: O(n + m)
    Space: O(1) - only rearranging pointers
    """
    dummy = ListNode(0)
    current = dummy

    while l1 and l2:
        if l1.val <= l2.val:
            current.next = l1
            l1 = l1.next
        else:
            current.next = l2
            l2 = l2.next
        current = current.next

    # Attach remaining nodes
    current.next = l1 if l1 else l2

    return dummy.next
```

### Visual Walkthrough

```
l1: [1] → [3] → [5]
l2: [2] → [4] → [6]

Step 1: 1 < 2, take 1
        dummy → [1]
                 ↑
               current

Step 2: 3 > 2, take 2
        dummy → [1] → [2]
                       ↑
                     current

Step 3: 3 < 4, take 3
        dummy → [1] → [2] → [3]

Step 4: 5 > 4, take 4
        dummy → [1] → [2] → [3] → [4]

Step 5: 5 < 6, take 5
        dummy → [1] → [2] → [3] → [4] → [5]

Step 6: l1 exhausted, attach remaining l2
        dummy → [1] → [2] → [3] → [4] → [5] → [6]

Result: [1] → [2] → [3] → [4] → [5] → [6]
```

---

## Recursive Merge Two Lists

```python
def merge_two_lists_recursive(l1: ListNode, l2: ListNode) -> ListNode:
    """
    Merge two sorted lists recursively.

    Time: O(n + m)
    Space: O(n + m) - call stack
    """
    if not l1:
        return l2
    if not l2:
        return l1

    if l1.val <= l2.val:
        l1.next = merge_two_lists_recursive(l1.next, l2)
        return l1
    else:
        l2.next = merge_two_lists_recursive(l1, l2.next)
        return l2
```

---

## Pattern 2: Merge K Sorted Lists

### Approach 1: Divide and Conquer

```python
def merge_k_lists(lists: list[ListNode]) -> ListNode:
    """
    Merge k sorted linked lists using divide and conquer.

    LeetCode 23: Merge k Sorted Lists

    Time: O(N log k) where N = total nodes, k = number of lists
    Space: O(log k) for recursion
    """
    if not lists:
        return None

    def merge_two(l1: ListNode, l2: ListNode) -> ListNode:
        dummy = ListNode(0)
        current = dummy

        while l1 and l2:
            if l1.val <= l2.val:
                current.next = l1
                l1 = l1.next
            else:
                current.next = l2
                l2 = l2.next
            current = current.next

        current.next = l1 if l1 else l2
        return dummy.next

    while len(lists) > 1:
        merged = []

        for i in range(0, len(lists), 2):
            l1 = lists[i]
            l2 = lists[i + 1] if i + 1 < len(lists) else None
            merged.append(merge_two(l1, l2))

        lists = merged

    return lists[0]
```

### Visual: Divide and Conquer

```
Lists: [L1, L2, L3, L4, L5, L6, L7, L8]

Round 1: Pair and merge
  L1+L2 → M1    L3+L4 → M2    L5+L6 → M3    L7+L8 → M4
  [M1, M2, M3, M4]

Round 2: Pair and merge
  M1+M2 → N1    M3+M4 → N2
  [N1, N2]

Round 3: Final merge
  N1+N2 → Result

Complexity: log k rounds, each round processes N total nodes
            = O(N log k)
```

### Approach 2: Priority Queue (Min-Heap)

```python
import heapq

def merge_k_lists_heap(lists: list[ListNode]) -> ListNode:
    """
    Merge k sorted linked lists using min-heap.

    Time: O(N log k)
    Space: O(k) for the heap
    """
    # Create min-heap with (value, index, node)
    # Index breaks ties (nodes aren't comparable)
    heap = []

    for i, node in enumerate(lists):
        if node:
            heapq.heappush(heap, (node.val, i, node))

    dummy = ListNode(0)
    current = dummy

    while heap:
        val, i, node = heapq.heappop(heap)
        current.next = node
        current = current.next

        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))

    return dummy.next
```

### Why Index is Needed in Heap

```python
# Without index, comparison of nodes with same value fails:
# heappush(heap, (5, node1))  # node1.val = 5
# heappush(heap, (5, node2))  # node2.val = 5
# TypeError: '<' not supported between 'ListNode' instances

# With index as tiebreaker:
# heappush(heap, (5, 0, node1))
# heappush(heap, (5, 1, node2))
# Works! Comparison: (5, 0, node1) < (5, 1, node2) → True
```

---

## Pattern 3: Merge Sort for Linked List

```python
def sort_list(head: ListNode) -> ListNode:
    """
    Sort linked list using merge sort.

    LeetCode 148: Sort List

    Time: O(n log n)
    Space: O(log n) for recursion (or O(1) with bottom-up approach)
    """
    # Base case
    if not head or not head.next:
        return head

    # Find middle and split
    left_half, right_half = split_list(head)

    # Recursively sort both halves
    left_sorted = sort_list(left_half)
    right_sorted = sort_list(right_half)

    # Merge sorted halves
    return merge_two_lists(left_sorted, right_sorted)


def split_list(head: ListNode) -> tuple:
    """Split list into two halves using fast-slow pointers."""
    slow = head
    fast = head.next  # Start fast one ahead for even split

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    second = slow.next
    slow.next = None  # Cut the connection

    return head, second


def merge_two_lists(l1: ListNode, l2: ListNode) -> ListNode:
    """Merge two sorted lists."""
    dummy = ListNode(0)
    current = dummy

    while l1 and l2:
        if l1.val <= l2.val:
            current.next = l1
            l1 = l1.next
        else:
            current.next = l2
            l2 = l2.next
        current = current.next

    current.next = l1 if l1 else l2
    return dummy.next
```

### Bottom-Up Merge Sort (O(1) Space)

```python
def sort_list_bottom_up(head: ListNode) -> ListNode:
    """
    Sort linked list using bottom-up merge sort.
    O(1) space (no recursion).

    Time: O(n log n)
    Space: O(1)
    """
    if not head or not head.next:
        return head

    # Get list length
    length = 0
    current = head
    while current:
        length += 1
        current = current.next

    dummy = ListNode(0)
    dummy.next = head
    size = 1

    while size < length:
        tail = dummy
        current = dummy.next

        while current:
            left = current
            right = split(left, size)
            current = split(right, size)
            tail = merge(left, right, tail)

        size *= 2

    return dummy.next


def split(head: ListNode, size: int) -> ListNode:
    """Split off 'size' nodes and return the remaining list."""
    for _ in range(size - 1):
        if not head:
            break
        head = head.next

    if not head:
        return None

    next_list = head.next
    head.next = None
    return next_list


def merge(l1: ListNode, l2: ListNode, tail: ListNode) -> ListNode:
    """Merge two lists and attach to tail. Return new tail."""
    while l1 and l2:
        if l1.val <= l2.val:
            tail.next = l1
            l1 = l1.next
        else:
            tail.next = l2
            l2 = l2.next
        tail = tail.next

    tail.next = l1 if l1 else l2

    while tail.next:
        tail = tail.next

    return tail
```

---

## Pattern 4: Add Two Numbers (Merge with Carry)

```python
def add_two_numbers(l1: ListNode, l2: ListNode) -> ListNode:
    """
    Add two numbers represented as linked lists (reverse order).

    LeetCode 2: Add Two Numbers

    Time: O(max(n, m))
    Space: O(max(n, m))
    """
    dummy = ListNode(0)
    current = dummy
    carry = 0

    while l1 or l2 or carry:
        val1 = l1.val if l1 else 0
        val2 = l2.val if l2 else 0

        total = val1 + val2 + carry
        carry = total // 10
        digit = total % 10

        current.next = ListNode(digit)
        current = current.next

        if l1:
            l1 = l1.next
        if l2:
            l2 = l2.next

    return dummy.next
```

### Add Two Numbers II (Forward Order)

```python
def add_two_numbers_ii(l1: ListNode, l2: ListNode) -> ListNode:
    """
    Add two numbers (forward order - most significant first).

    LeetCode 445: Add Two Numbers II

    Approach: Reverse both, add, reverse result.
    Time: O(n + m)
    Space: O(1) extra (modify in place)
    """
    def reverse(head: ListNode) -> ListNode:
        prev = None
        while head:
            next_temp = head.next
            head.next = prev
            prev = head
            head = next_temp
        return prev

    # Reverse both lists
    l1 = reverse(l1)
    l2 = reverse(l2)

    # Add (same as Add Two Numbers I)
    dummy = ListNode(0)
    current = dummy
    carry = 0

    while l1 or l2 or carry:
        val1 = l1.val if l1 else 0
        val2 = l2.val if l2 else 0

        total = val1 + val2 + carry
        carry = total // 10

        current.next = ListNode(total % 10)
        current = current.next

        if l1:
            l1 = l1.next
        if l2:
            l2 = l2.next

    # Reverse result
    return reverse(dummy.next)
```

---

## Complexity Comparison

| Approach | Time | Space |
|----------|------|-------|
| Merge two sorted | O(n + m) | O(1) |
| Merge k sorted (divide & conquer) | O(N log k) | O(log k) |
| Merge k sorted (heap) | O(N log k) | O(k) |
| Merge sort (recursive) | O(n log n) | O(log n) |
| Merge sort (bottom-up) | O(n log n) | O(1) |
| Add two numbers | O(max(n, m)) | O(max(n, m)) |

---

## Edge Cases

```python
# 1. One list is empty
merge_two_lists(None, l2)  # → l2
merge_two_lists(l1, None)  # → l1

# 2. Both lists empty
merge_two_lists(None, None)  # → None

# 3. Lists of different lengths
l1 = [1, 2]
l2 = [1, 2, 3, 4, 5]
# Merge continues until both exhausted

# 4. All elements same
l1 = [1, 1, 1]
l2 = [1, 1, 1]
# Stable merge: elements from l1 come first when equal

# 5. Single-element lists
l1 = [1]
l2 = [2]
# → [1, 2]

# 6. K lists with some empty
lists = [[1, 2], None, [3, 4], None]
# Filter or handle None gracefully
```

---

## Common Variations

### Merge Sorted Array (In-Place)

```python
def merge_lists_in_place(l1: ListNode, l2: ListNode) -> ListNode:
    """
    Merge two sorted lists by modifying pointers only.
    No new nodes created.
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

    tail.next = l1 or l2
    return dummy.next
```

### Insertion Sort List

```python
def insertion_sort_list(head: ListNode) -> ListNode:
    """
    Sort using insertion sort.

    LeetCode 147: Insertion Sort List

    Time: O(n²)
    Space: O(1)
    """
    dummy = ListNode(0)
    current = head

    while current:
        # Save next before we modify current.next
        next_temp = current.next

        # Find position to insert
        prev = dummy
        while prev.next and prev.next.val < current.val:
            prev = prev.next

        # Insert current after prev
        current.next = prev.next
        prev.next = current

        current = next_temp

    return dummy.next
```

---

## Practice Problems

| # | Problem | Difficulty | Key Concept |
|---|---------|------------|-------------|
| 1 | Merge Two Sorted Lists | Easy | Basic merge |
| 2 | Merge k Sorted Lists | Hard | Divide & conquer or heap |
| 3 | Sort List | Medium | Merge sort on linked list |
| 4 | Add Two Numbers | Medium | Merge with carry |
| 5 | Add Two Numbers II | Medium | Reverse + add |
| 6 | Insertion Sort List | Medium | Insertion sort variant |

---

## Key Takeaways

1. **Two-pointer merge** is O(n + m) time, O(1) space
2. **Merge K lists** with divide & conquer or heap: O(N log k)
3. **Merge sort on linked lists** is efficient: no random access needed
4. **Bottom-up merge sort** achieves O(1) space
5. **Add two numbers** is merge with carry logic
6. **Always use dummy node** to simplify head handling

---

## Next: [05-intersection-detection.md](./05-intersection-detection.md)

Learn how to find the intersection point of two linked lists.
