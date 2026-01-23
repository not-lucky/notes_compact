# Merge Operations

## Practice Problems

### 1. Merge Two Sorted Lists
**Difficulty:** Easy
**Key Technique:** Two pointers + dummy node

```python
def merge_two_lists(l1: ListNode, l2: ListNode) -> ListNode:
    """
    Time: O(n + m)
    Space: O(1)
    """
    dummy = ListNode(0)
    curr = dummy
    while l1 and l2:
        if l1.val <= l2.val:
            curr.next = l1
            l1 = l1.next
        else:
            curr.next = l2
            l2 = l2.next
        curr = curr.next
    curr.next = l1 or l2
    return dummy.next
```

### 2. Merge k Sorted Lists
**Difficulty:** Hard
**Key Technique:** Min-Heap or Divide and Conquer

```python
import heapq

def merge_k_lists(lists: list[ListNode]) -> ListNode:
    """
    Time: O(N log k) where N is total nodes, k is number of lists
    Space: O(k)
    """
    heap = []
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(heap, (node.val, i, node))

    dummy = ListNode(0)
    curr = dummy
    while heap:
        val, i, node = heapq.heappop(heap)
        curr.next = node
        curr = curr.next
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
    return dummy.next
```

### 3. Sort List
**Difficulty:** Medium
**Key Technique:** Merge Sort (Split + Merge)

```python
def sort_list(head: ListNode) -> ListNode:
    """
    Time: O(n log n)
    Space: O(log n)
    """
    if not head or not head.next: return head
    # Split
    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    mid = slow.next
    slow.next = None
    # Recurse
    left = sort_list(head)
    right = sort_list(mid)
    # Merge
    dummy = ListNode(0)
    curr = dummy
    while left and right:
        if left.val < right.val:
            curr.next, left = left, left.next
        else:
            curr.next, right = right, right.next
        curr = curr.next
    curr.next = left or right
    return dummy.next
```

### 4. Add Two Numbers
**Difficulty:** Medium
**Key Technique:** Traversal with carry

```python
def add_two_numbers(l1: ListNode, l2: ListNode) -> ListNode:
    """
    Time: O(max(N, M))
    Space: O(max(N, M))
    """
    dummy = ListNode(0)
    curr = dummy
    carry = 0
    while l1 or l2 or carry:
        v1 = l1.val if l1 else 0
        v2 = l2.val if l2 else 0
        val = v1 + v2 + carry
        carry = val // 10
        curr.next = ListNode(val % 10)
        curr = curr.next
        l1 = l1.next if l1 else None
        l2 = l2.next if l2 else None
    return dummy.next
```

### 5. Add Two Numbers II
**Difficulty:** Medium
**Key Technique:** Reverse + Add + Reverse (or Stack)

```python
def add_two_numbers_ii(l1: ListNode, l2: ListNode) -> ListNode:
    """
    Time: O(N + M)
    Space: O(1) (excluding output) if reversing in place
    """
    def reverse(h):
        prev, curr = None, h
        while curr:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        return prev

    l1, l2 = reverse(l1), reverse(l2)
    res = add_two_numbers(l1, l2) # Using logic from problem 4
    return reverse(res)
```
