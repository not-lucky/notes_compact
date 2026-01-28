# Solutions: Merge Operations

## 1. Merge Two Sorted Lists

**Problem Statement**: You are given the heads of two sorted linked lists `list1` and `list2`. Merge the two lists in a one sorted list. The list should be made by splicing together the nodes of the first two lists. Return the head of the merged linked list.

### Examples & Edge Cases

- **Example 1**: `list1 = [1,2,4], list2 = [1,3,4]` -> `[1,1,2,3,4,4]`
- **Example 2**: `list1 = [], list2 = []` -> `[]`
- **Example 3**: `list1 = [], list2 = [0]` -> `[0]`
- **Edge Case**: One list is significantly longer than the other.
- **Edge Case**: Lists contain duplicate values.

### Optimal Python Solution

```python
def mergeTwoLists(list1: ListNode, list2: ListNode) -> ListNode:
    """
    Iterative approach using a dummy node.
    We compare the heads of both lists and attach the smaller one to our result.
    """
    dummy = ListNode(0)
    current = dummy

    # While both lists have nodes, compare and pick the smaller one
    while list1 and list2:
        if list1.val <= list2.val:
            current.next = list1
            list1 = list1.next
        else:
            current.next = list2
            list2 = list2.next
        current = current.next

    # If one list is exhausted, attach the remainder of the other list
    current.next = list1 if list1 else list2

    return dummy.next
```

### Explanation

We use a `dummy` node to avoid handling the head as a special case. A `current` pointer tracks the end of our new merged list. We iterate as long as both lists have nodes, always picking the node with the smaller value. Once one list is empty, we simply point `current.next` to the remaining part of the other list.

### Complexity Analysis

- **Time Complexity**: O(n + m), where `n` and `m` are the lengths of the two lists. We visit each node exactly once.
- **Space Complexity**: O(1). We are only rearranging pointers, not creating new nodes.

---

## 2. Merge k Sorted Lists

**Problem Statement**: You are given an array of `k` linked-lists `lists`, each linked-list is sorted in ascending order. Merge all the linked-lists into one sorted linked-list and return it.

### Examples & Edge Cases

- **Example 1**: `[[1,4,5],[1,3,4],[2,6]]` -> `[1,1,2,3,4,4,5,6]`
- **Example 2**: `[]` -> `[]`
- **Example 3**: `[[]]` -> `[]`
- **Edge Case**: Some lists are empty within the input array.
- **Edge Case**: `k` is very large.

### Optimal Python Solution

```python
import heapq

def mergeKLists(lists: list[ListNode]) -> ListNode:
    """
    Using a Min-Heap to efficiently find the smallest element among k lists.
    """
    # Each entry in heap: (node_value, list_index, node_object)
    # list_index is used as a tie-breaker because ListNode is not comparable
    min_heap = []

    for i, head in enumerate(lists):
        if head:
            heapq.heappush(min_heap, (head.val, i, head))

    dummy = ListNode(0)
    curr = dummy

    while min_heap:
        val, i, node = heapq.heappop(min_heap)
        curr.next = node
        curr = curr.next

        # If the extracted node has a next node, push it into the heap
        if node.next:
            heapq.heappush(min_heap, (node.next.val, i, node.next))

    return dummy.next
```

### Explanation

We maintain a min-heap of size `k`, containing the current head of each of the `k` lists. In each step, we extract the smallest element from the heap, attach it to our result list, and then push the next node from that same list into the heap. This ensures we always have the next potential smallest element available in `O(log k)` time.

### Complexity Analysis

- **Time Complexity**: O(N log k), where `N` is the total number of nodes across all lists and `k` is the number of lists.
- **Space Complexity**: O(k) for the priority queue.

---

## 3. Sort List

**Problem Statement**: Given the `head` of a linked list, return the list after sorting it in ascending order. (Implement in O(n log n) time and O(1) space).

### Examples & Edge Cases

- **Example 1**: `head = [4,2,1,3]` -> `[1,2,3,4]`
- **Example 2**: `head = [-1,5,3,4,0]` -> `[-1,0,3,4,5]`
- **Edge Case**: Empty list.
- **Edge Case**: Already sorted list.

### Optimal Python Solution

```python
def sortList(head: ListNode) -> ListNode:
    """
    Merge Sort implementation for Linked Lists.
    Recursive approach (O(log n) stack space).
    """
    if not head or not head.next:
        return head

    # 1. Split the list into two halves
    left_half, right_half = split(head)

    # 2. Recursively sort both halves
    left = sortList(left_half)
    right = sortList(right_half)

    # 3. Merge sorted halves
    return merge(left, right)

def split(head):
    # Using fast-slow pointers to find the middle
    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    mid = slow.next
    slow.next = None # Break the link
    return head, mid

def merge(l1, l2):
    dummy = curr = ListNode(0)
    while l1 and l2:
        if l1.val < l2.val:
            curr.next, l1 = l1, l1.next
        else:
            curr.next, l2 = l2, l2.next
        curr = curr.next
    curr.next = l1 or l2
    return dummy.next
```

### Explanation

Merge Sort is ideal for linked lists because it doesn't require random access. We recursively split the list into two halves using the fast-slow pointer technique until we have single-node lists, then merge them back together in sorted order.

### Complexity Analysis

- **Time Complexity**: O(n log n). Standard merge sort complexity.
- **Space Complexity**: O(log n) due to the recursive call stack. (O(1) is possible using a bottom-up iterative approach).

---

## 4. Add Two Numbers

**Problem Statement**: You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.

### Examples & Edge Cases

- **Example 1**: `l1 = [2,4,3], l2 = [5,6,4]` -> `[7,0,8]` (342 + 465 = 807)
- **Example 2**: `l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]` -> `[8,9,9,9,0,0,0,1]`
- **Edge Case**: Lists of different lengths.
- **Edge Case**: A carry at the very end (e.g., 5 + 5 = 0 -> 1).

### Optimal Python Solution

```python
def addTwoNumbers(l1: ListNode, l2: ListNode) -> ListNode:
    dummy = ListNode(0)
    curr = dummy
    carry = 0

    # Continue until both lists are exhausted AND there's no remaining carry
    while l1 or l2 or carry:
        val1 = l1.val if l1 else 0
        val2 = l2.val if l2 else 0

        # Calculate sum and carry
        total = val1 + val2 + carry
        carry = total // 10
        out_val = total % 10

        # Create new node
        curr.next = ListNode(out_val)
        curr = curr.next

        # Move pointers forward
        if l1: l1 = l1.next
        if l2: l2 = l2.next

    return dummy.next
```

### Explanation

We iterate through both lists simultaneously, adding the values along with any carry from the previous step. If one list is shorter, we treat its missing values as 0. We continue until both lists are finished and any final carry has been processed.

### Complexity Analysis

- **Time Complexity**: O(max(n, m)), where `n` and `m` are the lengths of the two lists.
- **Space Complexity**: O(max(n, m)) for the new result list.

---

## 5. Add Two Numbers II

**Problem Statement**: Add two numbers where the most significant digit comes first.

### Examples & Edge Cases

- **Example**: `[7,2,4,3] + [5,6,4] = [7,8,0,7]`

### Optimal Python Solution

```python
def addTwoNumbers(l1: ListNode, l2: ListNode) -> ListNode:
    # 1. Reverse lists
    def reverse(node):
        prev = None
        while node:
            node.next, prev, node = prev, node, node.next
        return prev

    l1, l2 = reverse(l1), reverse(l2)

    # 2. Add (same as Add Two Numbers I)
    dummy = curr = ListNode(0)
    carry = 0
    while l1 or l2 or carry:
        v1 = l1.val if l1 else 0
        v2 = l2.val if l2 else 0
        carry, val = divmod(v1 + v2 + carry, 10)
        curr.next = ListNode(val)
        curr = curr.next
        if l1: l1 = l1.next
        if l2: l2 = l2.next

    # 3. Reverse result back
    return reverse(dummy.next)
```

### Explanation

Since we cannot easily add numbers from left to right (due to carry), we reverse the input lists, perform the standard addition, and then reverse the result back.

### Complexity Analysis

- **Time Complexity**: O(n + m).
- **Space Complexity**: O(max(n, m)).

---

## 6. Insertion Sort List

**Problem Statement**: Sort a linked list using insertion sort.

### Examples & Edge Cases

- **Example**: `[4,2,1,3]` -> `[1,2,3,4]`

### Optimal Python Solution

```python
def insertionSortList(head: ListNode) -> ListNode:
    """
    Simulate insertion sort by building a new sorted list.
    """
    dummy = ListNode(0)
    curr = head

    while curr:
        # Before we insert, save the next node to process
        next_to_process = curr.next

        # Find the insertion point in the sorted part (dummy)
        prev = dummy
        while prev.next and prev.next.val < curr.val:
            prev = prev.next

        # Insert curr between prev and prev.next
        curr.next = prev.next
        prev.next = curr

        # Move to the next node in the original list
        curr = next_to_process

    return dummy.next
```

### Explanation

We create a new sorted list (starting with a `dummy` node). For each node in the original list, we find its correct position in the new sorted list by traversing from the `dummy` head, and then we insert it.

### Complexity Analysis

- **Time Complexity**: O(n²). In the worst case (reverse sorted), we do O(n) work for each of the `n` nodes.
- **Space Complexity**: O(1). We reuse the existing nodes.
