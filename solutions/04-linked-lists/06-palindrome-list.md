# Solutions: Palindrome Linked List

## 1. Palindrome Linked List
**Problem Statement**: Given the `head` of a singly linked list, return `true` if it is a palindrome or `false` otherwise.

### Examples & Edge Cases
- **Example 1**: `head = [1,2,2,1]` -> `True`
- **Example 2**: `head = [1,2]` -> `False`
- **Edge Case**: Single node list (always `True`).
- **Edge Case**: Empty list (always `True`).
- **Edge Case**: Odd length list `[1,2,3,2,1]`.

### Optimal Python Solution
```python
def isPalindrome(head: ListNode) -> bool:
    """
    1. Find the middle of the list.
    2. Reverse the second half.
    3. Compare the first and second halves.
    4. (Optional) Restore the list.
    """
    if not head or not head.next:
        return True

    # 1. Find the end of the first half (middle)
    # Using fast-slow pointers
    slow = fast = head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next

    # 2. Reverse the second half
    # slow.next is the start of the second half
    second_half_head = reverseList(slow.next)

    # 3. Compare halves
    result = True
    p1 = head
    p2 = second_half_head
    while result and p2:
        if p1.val != p2.val:
            result = False
        p1 = p1.next
        p2 = p2.next

    # 4. Restore the original list
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
To achieve O(1) space, we can't copy the list. Instead, we find the midpoint. For a list of `n` nodes, `slow` will point to the `n/2`-th node. We then reverse the list starting from `slow.next`. This gives us two halves that we can compare element by element. After the comparison, we reverse the second half again to restore the original list structure.

### Complexity Analysis
- **Time Complexity**: O(n). We traverse the list to find the middle, reverse half, and compare. All are linear operations.
- **Space Complexity**: O(1). We perform all operations in-place.

---

## 2. Valid Palindrome
**Problem Statement**: Given a string `s`, return `true` if it is a palindrome, or `false` otherwise, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters.

### Examples & Edge Cases
- **Example 1**: `"A man, a plan, a canal: Panama"` -> `True`
- **Example 2**: `"race a car"` -> `False`

### Optimal Python Solution
```python
def isPalindrome(s: str) -> bool:
    left, right = 0, len(s) - 1

    while left < right:
        # Skip non-alphanumeric characters
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1

        if s[left].lower() != s[right].lower():
            return False

        left += 1
        right -= 1

    return True
```

### Explanation
We use two pointers, one at the start and one at the end of the string. We move them towards the center, skipping any characters that aren't letters or numbers. At each valid position, we compare the characters (case-insensitive). If they ever differ, it's not a palindrome.

### Complexity Analysis
- **Time Complexity**: O(n). We visit each character at most once.
- **Space Complexity**: O(1). We only use two pointers.

---

## 3. Valid Palindrome II
**Problem Statement**: Given a string `s`, return `true` if the `s` can be palindrome after deleting at most one character from it.

### Examples & Edge Cases
- **Example 1**: `"aba"` -> `True`
- **Example 2**: `"abca"` -> `True` (Delete 'c')
- **Example 3**: `"abc"` -> `False`

### Optimal Python Solution
```python
def validPalindrome(s: str) -> bool:
    def is_pali_range(i, j):
        return all(s[k] == s[j-k+i] for k in range(i, j))

    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            # Try skipping the character at 'left' or 'right'
            # and check if the remaining substring is a palindrome
            return s[left+1:right+1] == s[left+1:right+1][::-1] or \
                   s[left:right] == s[left:right][::-1]
        left += 1
        right -= 1
    return True
```

### Explanation
We use two pointers. When we find a mismatch, we have two choices: skip the left character or skip the right character. If either of the resulting substrings is a palindrome, then the original string is a "Valid Palindrome II".

### Complexity Analysis
- **Time Complexity**: O(n). In the worst case, we check two substrings of length nearly `n`.
- **Space Complexity**: O(n) for the substring slicing in Python, or O(1) if checked with a helper function using pointers.

---

## 4. Reorder List
**Problem Statement**: Reorder the list `L0 → L1 → … → Ln-1 → Ln` to `L0 → Ln → L1 → Ln-1 → L2 → Ln-2 → …`.

### Examples & Edge Cases
- **Example 1**: `[1,2,3,4]` -> `[1,4,2,3]`

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
Similar to the palindrome check, we split the list in half and reverse the second half. Instead of comparing them, we interleave the nodes from the two halves to achieve the desired "zigzag" order.

### Complexity Analysis
- **Time Complexity**: O(n).
- **Space Complexity**: O(1).
