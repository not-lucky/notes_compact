# Merge Two Sorted Lists

## Problem Statement

Merge two sorted linked lists and return it as a sorted list. The list should be made by splicing together the nodes of the first two lists.

**Example:**
```
Input: list1 = [1, 2, 4], list2 = [1, 3, 4]
Output: [1, 1, 2, 3, 4, 4]
```

## Approach

### Iterative with Dummy Node
1. Create a dummy node to simplify edge cases
2. Compare heads of both lists
3. Attach smaller node to result
4. Move pointer forward in that list
5. Append remaining list when one is exhausted

### Recursive
Base case: one list is empty, return the other.
Recursive case: attach smaller head and recurse.

## Implementation

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def merge_two_lists(list1: ListNode, list2: ListNode) -> ListNode:
    """
    Merge two sorted lists iteratively.

    Time: O(n + m)
    Space: O(1) - only using existing nodes
    """
    dummy = ListNode(0)
    current = dummy

    while list1 and list2:
        if list1.val <= list2.val:
            current.next = list1
            list1 = list1.next
        else:
            current.next = list2
            list2 = list2.next
        current = current.next

    # Attach remaining nodes
    current.next = list1 if list1 else list2

    return dummy.next


def merge_two_lists_recursive(list1: ListNode, list2: ListNode) -> ListNode:
    """
    Merge two sorted lists recursively.

    Time: O(n + m)
    Space: O(n + m) - recursion stack
    """
    if not list1:
        return list2
    if not list2:
        return list1

    if list1.val <= list2.val:
        list1.next = merge_two_lists_recursive(list1.next, list2)
        return list1
    else:
        list2.next = merge_two_lists_recursive(list1, list2.next)
        return list2
```

## Complexity Analysis

| Method | Time | Space | Notes |
|--------|------|-------|-------|
| Iterative | O(n + m) | O(1) | Optimal |
| Recursive | O(n + m) | O(n + m) | Stack space |

## Visual Walkthrough

```
list1: 1 → 2 → 4
list2: 1 → 3 → 4

Initial: dummy → ?
         curr = dummy

Step 1: Compare 1 vs 1
        Attach list1's 1
        dummy → 1
        list1 now: 2 → 4

Step 2: Compare 2 vs 1
        Attach list2's 1
        dummy → 1 → 1
        list2 now: 3 → 4

Step 3: Compare 2 vs 3
        Attach list1's 2
        dummy → 1 → 1 → 2
        list1 now: 4

Step 4: Compare 4 vs 3
        Attach list2's 3
        dummy → 1 → 1 → 2 → 3
        list2 now: 4

Step 5: Compare 4 vs 4
        Attach list1's 4
        dummy → 1 → 1 → 2 → 3 → 4
        list1 now: None

Step 6: list1 is None
        Attach remaining list2: 4
        dummy → 1 → 1 → 2 → 3 → 4 → 4

Return dummy.next
```

## Edge Cases

1. **Both empty**: Return None
2. **One empty**: Return the non-empty list
3. **Same values**: Handle ties consistently
4. **Already merged** (one list all smaller): Efficient attachment
5. **Single nodes**: Works correctly

## Common Mistakes

1. **Forgetting to advance current**: `current = current.next`
2. **Not handling empty lists**: Check before while loop
3. **Losing reference to head**: Use dummy node
4. **Infinite loop**: Make sure to advance list pointers

## Why Dummy Node?

Without dummy node, we need special handling for the first node:
```python
# Without dummy - messier code
def merge_without_dummy(list1, list2):
    if not list1:
        return list2
    if not list2:
        return list1

    if list1.val <= list2.val:
        head = list1
        list1 = list1.next
    else:
        head = list2
        list2 = list2.next

    current = head
    # ... rest of logic
```

With dummy node, the first node is handled the same as others.

## Variations

### Merge K Sorted Lists
```python
import heapq

def merge_k_lists(lists: list[ListNode]) -> ListNode:
    """
    Merge k sorted lists using min-heap.

    Time: O(N log k) - N total nodes, k lists
    Space: O(k) - heap size
    """
    # Custom comparison for ListNode
    ListNode.__lt__ = lambda self, other: self.val < other.val

    heap = []
    for lst in lists:
        if lst:
            heapq.heappush(heap, lst)

    dummy = ListNode(0)
    current = dummy

    while heap:
        node = heapq.heappop(heap)
        current.next = node
        current = current.next

        if node.next:
            heapq.heappush(heap, node.next)

    return dummy.next


def merge_k_lists_divide_conquer(lists: list[ListNode]) -> ListNode:
    """
    Merge k sorted lists using divide and conquer.

    Time: O(N log k)
    Space: O(log k) - recursion depth
    """
    if not lists:
        return None

    def merge_two(l1, l2):
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

    while len(lists) > 1:
        merged = []
        for i in range(0, len(lists), 2):
            l1 = lists[i]
            l2 = lists[i + 1] if i + 1 < len(lists) else None
            merged.append(merge_two(l1, l2))
        lists = merged

    return lists[0]
```

### Sort List (Merge Sort)
```python
def sort_list(head: ListNode) -> ListNode:
    """
    Sort linked list using merge sort.

    Time: O(n log n)
    Space: O(log n) - recursion stack
    """
    if not head or not head.next:
        return head

    # Find middle
    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    # Split
    mid = slow.next
    slow.next = None

    # Sort halves
    left = sort_list(head)
    right = sort_list(mid)

    # Merge
    return merge_two_lists(left, right)
```

### Add Two Numbers (Linked List)
```python
def add_two_numbers(l1: ListNode, l2: ListNode) -> ListNode:
    """
    Add two numbers represented as reversed linked lists.

    Example: 342 + 465 = 807
    Input: 2→4→3, 5→6→4
    Output: 7→0→8
    """
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

        l1 = l1.next if l1 else None
        l2 = l2.next if l2 else None

    return dummy.next
```

## Related Problems

- **Merge K Sorted Lists** - Generalization with heap
- **Sort List** - Merge sort on linked list
- **Add Two Numbers** - Similar traversal pattern
- **Intersection of Two Linked Lists** - Two-pointer on lists
- **Reorder List** - Combines split, reverse, and merge
