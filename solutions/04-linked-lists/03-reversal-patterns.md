# Solutions: Reversal Patterns

## 1. Reverse Linked List
**Problem Statement**: Given the `head` of a singly linked list, reverse the list, and return the reversed list.

### Examples & Edge Cases
- **Example 1**: `head = [1,2,3,4,5]` -> `[5,4,3,2,1]`
- **Example 2**: `head = [1,2]` -> `[2,1]`
- **Example 3**: `head = []` -> `[]`
- **Edge Case**: Empty list.
- **Edge Case**: Single node list.

### Optimal Python Solution
```python
def reverseList(head: ListNode) -> ListNode:
    """
    Iterative approach using three pointers: prev, curr, and next_node.
    """
    prev = None
    curr = head

    while curr:
        # Save the next node before we break the link
        next_node = curr.next
        # Reverse the current node's pointer
        curr.next = prev
        # Move pointers forward
        prev = curr
        curr = next_node

    return prev
```

### Explanation
We maintain three pointers. `curr` is the node we are currently processing. `prev` is the node that will become `curr.next`. Before we update `curr.next`, we must save the original `curr.next` in `next_node` so we don't lose the rest of the list. After the loop, `prev` will be pointing to the new head of the reversed list.

### Complexity Analysis
- **Time Complexity**: O(n). We visit each node exactly once.
- **Space Complexity**: O(1). We only use three pointers regardless of list size.

---

## 2. Reverse Linked List II
**Problem Statement**: Given the `head` of a singly linked list and two integers `left` and `right` where `left <= right`, reverse the nodes of the list from position `left` to position `right`, and return the reversed list.

### Examples & Edge Cases
- **Example 1**: `head = [1,2,3,4,5], left = 2, right = 4` -> `[1,4,3,2,5]`
- **Example 2**: `head = [5], left = 1, right = 1` -> `[5]`
- **Edge Case**: `left == right` (no change).
- **Edge Case**: `left == 1` (reversing from the head).
- **Edge Case**: Reversing the entire list.

### Optimal Python Solution
```python
def reverseBetween(head: ListNode, left: int, right: int) -> ListNode:
    if not head or left == right:
        return head

    dummy = ListNode(0, head)
    prev = dummy

    # 1. Reach the node just before the 'left' position
    for _ in range(left - 1):
        prev = prev.next

    # 2. Reverse 'right - left' nodes
    # curr is the node that will stay at the end of the reversed segment
    curr = prev.next
    for _ in range(right - left):
        temp = curr.next
        curr.next = temp.next
        temp.next = prev.next
        prev.next = temp

    return dummy.next
```

### Explanation
We use a dummy node to handle the case where `left = 1`. We first move `prev` to the node at position `left-1`. Then, we perform a sub-reversal. Instead of a full three-pointer reversal, we use a "pull-to-front" strategy: for each node in the range, we move it to be the new `prev.next`.

### Complexity Analysis
- **Time Complexity**: O(n). We traverse to the `left` position and then reverse up to `right`.
- **Space Complexity**: O(1). Only a few pointers and a dummy node are used.

---

## 3. Swap Nodes in Pairs
**Problem Statement**: Given a linked list, swap every two adjacent nodes and return its head. You must solve the problem without modifying the values in the list's nodes (i.e., only nodes themselves may be changed).

### Examples & Edge Cases
- **Example 1**: `head = [1,2,3,4]` -> `[2,1,4,3]`
- **Example 2**: `head = []` -> `[]`
- **Example 3**: `head = [1]` -> `[1]`
- **Edge Case**: Odd number of nodes (last node remains in place).

### Optimal Python Solution
```python
def swapPairs(head: ListNode) -> ListNode:
    dummy = ListNode(0, head)
    prev = dummy

    while prev.next and prev.next.next:
        # Nodes to be swapped
        first = prev.next
        second = prev.next.next

        # Swapping logic
        first.next = second.next
        second.next = first
        prev.next = second

        # Move prev forward by two nodes (now 'first')
        prev = first

    return dummy.next
```

### Explanation
We use a `dummy` node to simplify head management. In each step, we identify two nodes (`first` and `second`). We point `first.next` to the node after `second`, `second.next` to `first`, and the previous node's `next` to `second`.

### Complexity Analysis
- **Time Complexity**: O(n). We visit each pair once.
- **Space Complexity**: O(1). No extra space used besides pointers.

---

## 4. Reverse Nodes in k-Group
**Problem Statement**: Given the `head` of a linked list, reverse the nodes of the list `k` at a time, and return the modified list. `k` is a positive integer and is less than or equal to the length of the linked list. If the number of nodes is not a multiple of `k` then left-out nodes, in the end, should remain as it is.

### Examples & Edge Cases
- **Example 1**: `head = [1,2,3,4,5], k = 2` -> `[2,1,4,3,5]`
- **Example 2**: `head = [1,2,3,4,5], k = 3` -> `[3,2,1,4,5]`
- **Edge Case**: `k = 1` (no change).
- **Edge Case**: List length is a multiple of `k`.
- **Edge Case**: List length is less than `k`.

### Optimal Python Solution
```python
def reverseKGroup(head: ListNode, k: int) -> ListNode:
    dummy = ListNode(0, head)
    groupPrev = dummy

    while True:
        kth = getKth(groupPrev, k)
        if not kth:
            break
        groupNext = kth.next

        # Reverse the group
        prev, curr = kth.next, groupPrev.next
        while curr != groupNext:
            tmp = curr.next
            curr.next = prev
            prev = curr
            curr = tmp

        # Connect with previous group
        tmp = groupPrev.next
        groupPrev.next = kth
        groupPrev = tmp

    return dummy.next

def getKth(curr, k):
    while curr and k > 0:
        curr = curr.next
        k -= 1
    return curr
```

### Explanation
We process the list in groups of `k`. First, we find the `k`-th node. If it doesn't exist, we've reached the end and stop. Otherwise, we reverse the `k` nodes and reconnect them to the `groupPrev` and the start of the next group (`groupNext`).

### Complexity Analysis
- **Time Complexity**: O(n). Each node is visited twice (once to find the `k`-th node, once to reverse).
- **Space Complexity**: O(1). Iterative solution uses no extra stack space.

---

## 5. Rotate List
**Problem Statement**: Given the `head` of a linked list, rotate the list to the right by `k` places.

### Examples & Edge Cases
- **Example 1**: `head = [1,2,3,4,5], k = 2` -> `[4,5,1,2,3]`
- **Example 2**: `head = [0,1,2], k = 4` -> `[2,0,1]`
- **Edge Case**: `k = 0`.
- **Edge Case**: `k` is a multiple of list length (no change).
- **Edge Case**: Empty list or single node.

### Optimal Python Solution
```python
def rotateRight(head: ListNode, k: int) -> ListNode:
    if not head or not head.next or k == 0:
        return head

    # 1. Compute length and find tail
    old_tail = head
    length = 1
    while old_tail.next:
        old_tail = old_tail.next
        length += 1

    # 2. Connect tail to head to make it circular
    old_tail.next = head

    # 3. Find new tail: (length - k % length - 1)th node
    # and new head: (length - k % length)th node
    new_tail = head
    for _ in range(length - (k % length) - 1):
        new_tail = new_tail.next
    new_head = new_tail.next

    # 4. Break the circle
    new_tail.next = None

    return new_head
```

### Explanation
First, we find the length of the list and turn it into a circular linked list by connecting the tail to the head. The new head will be at position `length - (k % length)`. We find the node just before it, make it the new tail (pointing to `None`), and return the new head.

### Complexity Analysis
- **Time Complexity**: O(n). We traverse the list once to find length/tail and then a partial traversal to find the new tail.
- **Space Complexity**: O(1). No extra space used.

---

## 6. Reorder List
**Problem Statement**: Reorder the list `L0 → L1 → … → Ln-1 → Ln` to `L0 → Ln → L1 → Ln-1 → L2 → Ln-2 → …`.

### Examples & Edge Cases
- **Example 1**: `[1,2,3,4]` -> `[1,4,2,3]`
- **Example 2**: `[1,2,3,4,5]` -> `[1,5,2,4,3]`

### Optimal Python Solution
```python
def reorderList(head: ListNode) -> None:
    if not head: return

    # 1. Find middle
    slow, fast = head, head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    # 2. Reverse second half
    prev, curr = None, slow
    while curr:
        curr.next, prev, curr = prev, curr, curr.next

    # 3. Merge two halves
    first, second = head, prev
    while second.next:
        first.next, first = second, first.next
        second.next, second = first, second.next
```

### Explanation
This problem is a masterclass in combining patterns: 1) Find the middle with fast-slow pointers. 2) Reverse the second half of the list. 3) Interleave the two halves.

### Complexity Analysis
- **Time Complexity**: O(n). Each step is linear.
- **Space Complexity**: O(1). In-place modification.

---

## 7. Add Two Numbers II
**Problem Statement**: You are given two non-empty linked lists representing two non-negative integers. The most significant digit comes first and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.

### Examples & Edge Cases
- **Example 1**: `l1 = [7,2,4,3], l2 = [5,6,4]` -> `[7,8,0,7]`
- **Example 2**: `l1 = [2,4,3], l2 = [5,6,4]` -> `[8,0,7]`
- **Edge Case**: Resulting number has an extra carry at the beginning (e.g., 5+5=10).

### Optimal Python Solution
```python
def addTwoNumbers(l1: ListNode, l2: ListNode) -> ListNode:
    # 1. Reverse both lists to add from least significant digit
    def reverse(head):
        prev = None
        while head:
            head.next, prev, head = prev, head, head.next
        return prev

    l1 = reverse(l1)
    l2 = reverse(l2)

    # 2. Add numbers
    head = None
    carry = 0
    while l1 or l2 or carry:
        val1 = l1.val if l1 else 0
        val2 = l2.val if l2 else 0
        l1 = l1.next if l1 else None
        l2 = l2.next if l2 else None

        carry, val = divmod(val1 + val2 + carry, 10)
        # 3. Build result list from tail to head to avoid extra reverse
        head = ListNode(val, head)

    return head
```

### Explanation
Addition is easiest from the least significant digit (the end). We reverse both lists, perform the addition with carry, and build the resulting list backwards (prepending new nodes) so that the most significant digit ends up at the head.

### Complexity Analysis
- **Time Complexity**: O(n + m). Reversing and adding are linear with respect to list lengths.
- **Space Complexity**: O(max(n, m)). Space for the resulting linked list.
