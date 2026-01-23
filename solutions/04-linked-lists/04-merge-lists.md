# Solution: Merge Operations Practice Problems

## Problem 1: Merge Two Sorted Lists
### Problem Statement
You are given the heads of two sorted linked lists `list1` and `list2`. Merge the two lists in a one sorted list. The list should be made by splicing together the nodes of the first two lists. Return the head of the merged linked list.

### Constraints
- The number of nodes in both lists is in the range `[0, 50]`.
- `-100 <= Node.val <= 100`
- Both `list1` and `list2` are sorted in non-decreasing order.

### Example
Input: `list1 = [1,2,4], list2 = [1,3,4]`
Output: `[1,1,2,3,4,4]`

### Python Implementation
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def mergeTwoLists(list1: ListNode, list2: ListNode) -> ListNode:
    """
    Time Complexity: O(n + m)
    Space Complexity: O(1)
    """
    dummy = ListNode()
    curr = dummy

    while list1 and list2:
        if list1.val < list2.val:
            curr.next = list1
            list1 = list1.next
        else:
            curr.next = list2
            list2 = list2.next
        curr = curr.next

    curr.next = list1 or list2
    return dummy.next
```

---

## Problem 2: Merge k Sorted Lists
### Problem Statement
You are given an array of `k` linked-lists `lists`, each linked-list is sorted in ascending order. Merge all the linked-lists into one sorted linked-list and return it.

### Constraints
- `k == lists.length`
- `0 <= k <= 10^4`
- `0 <= lists[i].length <= 500`
- `-10^4 <= lists[i][j] <= 10^4`
- `lists[i]` is sorted in ascending order.
- The sum of `lists[i].length` will not exceed `10^4`.

### Example
Input: `lists = [[1,4,5],[1,3,4],[2,6]]`
Output: `[1,1,2,3,4,4,5,6]`

### Python Implementation
```python
import heapq

def mergeKLists(lists: list[ListNode]) -> ListNode:
    """
    Time Complexity: O(N log k) where N is total nodes, k is number of lists
    Space Complexity: O(k) for heap
    """
    heap = []
    for i, l in enumerate(lists):
        if l:
            heapq.heappush(heap, (l.val, i, l))

    dummy = ListNode()
    curr = dummy

    while heap:
        val, i, node = heapq.heappop(heap)
        curr.next = node
        curr = curr.next
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))

    return dummy.next
```

---

## Problem 3: Sort List
### Problem Statement
Given the head of a linked list, return the list after sorting it in ascending order. Solve it in `O(n log n)` time and `O(1)` memory (excluding recursion stack).

### Constraints
- The number of nodes in the list is in the range `[0, 5 * 10^4]`.
- `-10^5 <= Node.val <= 10^5`

### Example
Input: `head = [4,2,1,3]`
Output: `[1,2,3,4]`

### Python Implementation
```python
def sortList(head: ListNode) -> ListNode:
    """
    Time Complexity: O(n log n)
    Space Complexity: O(log n) for recursion
    """
    if not head or not head.next:
        return head

    # Split the list
    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    mid = slow.next
    slow.next = None

    # Sort recursively
    left = sortList(head)
    right = sortList(mid)

    # Merge
    dummy = ListNode()
    curr = dummy
    while left and right:
        if left.val < right.val:
            curr.next = left
            left = left.next
        else:
            curr.next = right
            right = right.next
        curr = curr.next
    curr.next = left or right

    return dummy.next
```

---

## Problem 4: Add Two Numbers
### Problem Statement
You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.

### Constraints
- The number of nodes in each linked list is in the range `[1, 100]`.
- `0 <= Node.val <= 9`
- It is guaranteed that the list represents a number that does not have leading zeros, except the number 0 itself.

### Example
Input: `l1 = [2,4,3], l2 = [5,6,4]`
Output: `[7,0,8]` (342 + 465 = 807)

### Python Implementation
```python
def addTwoNumbers(l1: ListNode, l2: ListNode) -> ListNode:
    """
    Time Complexity: O(max(n, m))
    Space Complexity: O(max(n, m))
    """
    dummy = ListNode()
    curr = dummy
    carry = 0

    while l1 or l2 or carry:
        v1 = l1.val if l1 else 0
        v2 = l2.val if l2 else 0

        total = v1 + v2 + carry
        carry = total // 10
        curr.next = ListNode(total % 10)

        curr = curr.next
        if l1: l1 = l1.next
        if l2: l2 = l2.next

    return dummy.next
```
