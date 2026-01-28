# Solutions: Fast-Slow Pointers

## 1. Middle of the Linked List

**Problem Statement**: Given the `head` of a singly linked list, return the middle node of the linked list. If there are two middle nodes, return the second middle node.

### Examples & Edge Cases

- **Example 1**: `head = [1,2,3,4,5]` -> `[3,4,5]`
- **Example 2**: `head = [1,2,3,4,5,6]` -> `[4,5,6]`
- **Edge Case**: Single node list.
- **Edge Case**: Two node list.

### Optimal Python Solution

```python
def middleNode(head: ListNode) -> ListNode:
    """
    Two pointers: slow and fast.
    Fast moves twice as fast as slow.
    When fast reaches the end, slow is at the middle.
    """
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow
```

### Explanation

By moving `fast` at twice the speed of `slow`, we ensure that when `fast` has covered the entire distance `n`, `slow` has covered `n/2`. For even-length lists, the condition `while fast and fast.next` ensures `slow` lands on the second middle node.

### Complexity Analysis

- **Time Complexity**: O(n). We traverse the list once.
- **Space Complexity**: O(1). Only two pointers are used.

---

## 2. Linked List Cycle

**Problem Statement**: Given `head`, the head of a linked list, determine if the linked list has a cycle in it. There is a cycle in a linked list if there is some node in the list that can be reached again by continuously following the `next` pointer.

### Examples & Edge Cases

- **Example 1**: `head = [3,2,0,-4], pos = 1` -> `True`
- **Example 2**: `head = [1,2], pos = 0` -> `True`
- **Example 3**: `head = [1], pos = -1` -> `False`
- **Edge Case**: Empty list.
- **Edge Case**: List with one node and no cycle.
- **Edge Case**: List with one node pointing to itself (cycle).

### Optimal Python Solution

```python
def hasCycle(head: ListNode) -> bool:
    """
    Floyd's Cycle-Finding Algorithm.
    If a cycle exists, the fast pointer will eventually catch up
    to the slow pointer inside the loop.
    """
    if not head:
        return False

    slow = head
    fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

        if slow == fast:
            return True

    return False
```

### Explanation

This is the classic "Tortoise and Hare" algorithm. If there is no cycle, the fast pointer will reach the end (`None`). If there is a cycle, the fast pointer will enter the cycle first, followed by the slow pointer. Once both are in the cycle, the gap between them decreases by 1 each step until they meet.

### Complexity Analysis

- **Time Complexity**: O(n). In the worst case (a cycle), the fast pointer will catch the slow pointer in linear time relative to the number of nodes.
- **Space Complexity**: O(1). No extra memory is used.

---

## 3. Linked List Cycle II

**Problem Statement**: Given the `head` of a linked list, return the node where the cycle begins. If there is no cycle, return `null`.

### Examples & Edge Cases

- **Example 1**: `head = [3,2,0,-4], pos = 1` -> `Node(2)`
- **Example 2**: `head = [1,2], pos = 0` -> `Node(1)`
- **Edge Case**: List with no cycle.
- **Edge Case**: Cycle starts at the head.

### Optimal Python Solution

```python
def detectCycle(head: ListNode) -> ListNode:
    """
    Phase 1: Detect if a cycle exists.
    Phase 2: Reset one pointer to head and move both at speed 1 to find start.
    """
    slow = fast = head

    # Phase 1: Detection
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            # Cycle detected
            # Phase 2: Find entrance
            slow = head
            while slow != fast:
                slow = slow.next
                fast = fast.next
            return slow

    return None
```

### Explanation

The math works as follows: Let `L1` be distance from head to cycle start, `L2` be distance from start to meeting point, and `C` be cycle length.

- Slow distance: `L1 + L2`
- Fast distance: `L1 + L2 + n*C`
- `2(L1 + L2) = L1 + L2 + n*C` => `L1 + L2 = n*C` => `L1 = n*C - L2`.
  This means the distance from head to start (`L1`) is the same as moving from meeting point `n` times around the cycle minus `L2`. Thus, they meet at the entrance.

### Complexity Analysis

- **Time Complexity**: O(n). Two linear passes (one to find meeting point, one to find entrance).
- **Space Complexity**: O(1). Only two pointers used.

---

## 4. Remove Nth Node From End

**Problem Statement**: Given the `head` of a linked list, remove the `n`-th node from the end of the list and return its head.

### Examples & Edge Cases

- **Example 1**: `head = [1,2,3,4,5], n = 2` -> `[1,2,3,5]`
- **Example 2**: `head = [1], n = 1` -> `[]`
- **Example 3**: `head = [1,2], n = 1` -> `[1]`
- **Edge Case**: Removing the head node (`n` equals length of list).
- **Edge Case**: Removing the tail node (`n = 1`).

### Optimal Python Solution

```python
def removeNthFromEnd(head: ListNode, n: int) -> ListNode:
    """
    Maintain a gap of 'n' between two pointers.
    When the forward pointer reaches the end, the back pointer
    is at the node before the one to be removed.
    """
    dummy = ListNode(0, head)
    first = dummy
    second = dummy

    # Advance first pointer so that the gap between first and second is n nodes
    for _ in range(n + 1):
        first = first.next

    # Move first to the end, maintaining the gap
    while first:
        first = first.next
        second = second.next

    # second is now before the node to be removed
    second.next = second.next.next

    return dummy.next
```

### Explanation

We use a `dummy` node to simplify the case where the head is removed. By moving `first` pointer `n+1` steps ahead, we establish a gap. When `first` hits `None`, `second` is exactly at the node _preceding_ the target. We then just skip the target node.

### Complexity Analysis

- **Time Complexity**: O(n). We traverse the list exactly once.
- **Space Complexity**: O(1). Only pointers and a dummy node.

---

## 5. Palindrome Linked List

**Problem Statement**: Given the `head` of a singly linked list, return `true` if it is a palindrome or `false` otherwise.

### Examples & Edge Cases

- **Example 1**: `head = [1,2,2,1]` -> `True`
- **Example 2**: `head = [1,2]` -> `False`
- **Edge Case**: Single node list (always true).
- **Edge Case**: Even vs Odd number of nodes.

### Optimal Python Solution

```python
def isPalindrome(head: ListNode) -> bool:
    if not head or not head.next:
        return True

    # 1. Find the end of first half
    slow = fast = head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next

    # 2. Reverse the second half
    second_half_head = reverseList(slow.next)

    # 3. Check for palindrome
    result = True
    first_half_ptr = head
    second_half_ptr = second_half_head
    while result and second_half_ptr:
        if first_half_ptr.val != second_half_ptr.val:
            result = False
        first_half_ptr = first_half_ptr.next
        second_half_ptr = second_half_ptr.next

    # 4. Restore the list (optional)
    slow.next = reverseList(second_half_head)

    return result

def reverseList(head):
    prev = None
    curr = head
    while curr:
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node
    return prev
```

### Explanation

To check for a palindrome in O(1) space, we:

1. Find the middle using fast-slow pointers.
2. Reverse the second half of the list.
3. Compare the first half with the reversed second half.
4. (Optional) Reverse back the second half to keep the original structure.

### Complexity Analysis

- **Time Complexity**: O(n). Finding middle, reversing, and comparing all take linear time.
- **Space Complexity**: O(1). We modify the list in place without extra structures.

---

## 6. Reorder List

**Problem Statement**: You are given the head of a singly linked-list. The list can be represented as: `L0 → L1 → … → Ln - 1 → Ln`. Reorder the list to be on the following form: `L0 → Ln → L1 → Ln - 1 → L2 → Ln - 2 → …`

### Examples & Edge Cases

- **Example 1**: `[1,2,3,4]` -> `[1,4,2,3]`
- **Example 2**: `[1,2,3,4,5]` -> `[1,5,2,4,3]`
- **Edge Case**: List with 1 or 2 nodes (no change).

### Optimal Python Solution

```python
def reorderList(head: ListNode) -> None:
    if not head:
        return

    # 1. Find middle
    slow = fast = head
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

This is a combination of finding the middle, reversing a list, and merging two lists. We find the middle point, reverse the second half, and then interleave the nodes from the two halves until they meet.

### Complexity Analysis

- **Time Complexity**: O(n). All three steps (finding middle, reversing, merging) are O(n).
- **Space Complexity**: O(1). Only pointers are used.

---

## 7. Happy Number

**Problem Statement**: Write an algorithm to determine if a number `n` is happy. A happy number is a number defined by the following process: Starting with any positive integer, replace the number by the sum of the squares of its digits. Repeat the process until the number equals 1 (where it will stay), or it loops endlessly in a cycle which does not include 1. Those numbers for which this process ends in 1 are happy.

### Examples & Edge Cases

- **Example 1**: `n = 19` -> `True` (1^2 + 9^2 = 82; 8^2 + 2^2 = 68; 6^2 + 8^2 = 100; 1^2 + 0^2 + 0^2 = 1)
- **Example 2**: `n = 2` -> `False`
- **Edge Case**: Cycle that doesn't include 1.

### Optimal Python Solution

```python
def isHappy(n: int) -> bool:
    """
    We treat the sequence of numbers as a linked list.
    If there is a cycle (Floyd's), it's not a happy number.
    """
    def get_next(number):
        total_sum = 0
        while number > 0:
            number, digit = divmod(number, 10)
            total_sum += digit ** 2
        return total_sum

    slow = n
    fast = get_next(n)

    while fast != 1 and slow != fast:
        slow = get_next(slow)
        fast = get_next(get_next(fast))

    return fast == 1
```

### Explanation

While not a linked list problem in the data-structure sense, the sequence of numbers follows the same logic. We use fast-slow pointers to detect if we've entered a cycle. If `fast` hits 1, the number is happy. If `slow` meets `fast` and neither is 1, it's a cycle and not happy.

### Complexity Analysis

- **Time Complexity**: O(log n). The number of digits in `n` is `log10(n)`, and the sum of squares reduces the number quickly.
- **Space Complexity**: O(1). No extra memory used besides a few variables.
