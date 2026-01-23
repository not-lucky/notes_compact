# Solution: Palindrome Linked List Practice Problems

## Problem 1: Palindrome Linked List
### Problem Statement
Given the head of a singly linked list, return true if it is a palindrome or false otherwise.

### Constraints
- The number of nodes in the list is in the range `[1, 10^5]`.
- `0 <= Node.val <= 9`

### Example
Input: `head = [1,2,2,1]`
Output: `true`

### Python Implementation
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def isPalindrome(head: ListNode) -> bool:
    """
    Time Complexity: O(n)
    Space Complexity: O(1)

    1. Find middle.
    2. Reverse second half.
    3. Compare first and second halves.
    """
    if not head or not head.next:
        return True

    # Find middle
    slow = fast = head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next

    # Reverse second half
    def reverse(node):
        prev = None
        while node:
            nxt = node.next
            node.next = prev
            prev = node
            node = nxt
        return prev

    second_half = reverse(slow.next)

    # Compare
    first_half = head
    while second_half:
        if first_half.val != second_half.val:
            return False
        first_half = first_half.next
        second_half = second_half.next

    return True
```

---

## Problem 2: Valid Palindrome
### Problem Statement
A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward. Alphanumeric characters include letters and numbers. Given a string `s`, return true if it is a palindrome, or false otherwise.

### Constraints
- `1 <= s.length <= 2 * 10^5`
- `s` consists only of printable ASCII characters.

### Example
Input: `s = "A man, a plan, a canal: Panama"`
Output: `true`

### Python Implementation
```python
def isPalindromeString(s: str) -> bool:
    """
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    l, r = 0, len(s) - 1
    while l < r:
        if not s[l].isalnum():
            l += 1
        elif not s[r].isalnum():
            r -= 1
        else:
            if s[l].lower() != s[r].lower():
                return False
            l += 1
            r -= 1
    return True
```

---

## Problem 3: Valid Palindrome II
### Problem Statement
Given a string `s`, return true if the `s` can be palindrome after deleting at most one character from it.

### Constraints
- `1 <= s.length <= 10^5`
- `s` consists of lowercase English letters.

### Example
Input: `s = "aba"`
Output: `true`

### Python Implementation
```python
def validPalindrome(s: str) -> bool:
    """
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    def check(l, r):
        while l < r:
            if s[l] != s[r]:
                return False
            l += 1
            r -= 1
        return True

    l, r = 0, len(s) - 1
    while l < r:
        if s[l] != s[r]:
            # Try deleting s[l] or s[r]
            return check(l + 1, r) or check(l, r - 1)
        l += 1
        r -= 1
    return True
```

---

## Problem 4: Reorder List
### Problem Statement
You are given the head of a singly linked-list. The list can be represented as: `L0 → L1 → … → Ln - 1 → Ln`. Reorder the list to be on the following form: `L0 → Ln → L1 → Ln - 1 → L2 → Ln - 2 → …`.

### Constraints
- The number of nodes in the list is in the range `[1, 5 * 10^4]`.
- `1 <= Node.val <= 1000`

### Example
Input: `head = [1,2,3,4]`
Output: `[1,4,2,3]`

### Python Implementation
```python
def reorderList(head: ListNode) -> None:
    """
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    if not head or not head.next:
        return

    # 1. Find middle
    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    # 2. Reverse second half
    curr = slow.next
    slow.next = None
    prev = None
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt

    # 3. Merge two halves
    first, second = head, prev
    while second:
        tmp1, tmp2 = first.next, second.next
        first.next = second
        second.next = tmp1
        first, second = tmp1, tmp2
```
