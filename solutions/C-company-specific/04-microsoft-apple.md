# Microsoft & Apple Interview Patterns

## Practice Problems

### 1. Reverse Linked List
**Difficulty:** Easy
**Key Technique:** Iterative reversal (Microsoft: Collaborative problem decomposition)

```python
def reverse_list(head):
    """
    Time: O(n)
    Space: O(1)
    """
    prev = None
    curr = head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev
```

### 2. Lowest Common Ancestor of a Binary Tree
**Difficulty:** Medium
**Key Technique:** Recursion (Microsoft: Handling ambiguity methodically)

```python
def lowest_common_ancestor(root, p, q):
    """
    Time: O(n)
    Space: O(h) where h is height
    """
    if not root or root == p or root == q:
        return root
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    if left and right: return root
    return left if left else right
```

### 3. Valid Number
**Difficulty:** Hard
**Key Technique:** String parsing (Apple: Handling every edge case)

```python
def is_number(s: str) -> bool:
    """
    Time: O(n)
    Space: O(1)
    """
    s = s.strip()
    met_dot = met_e = met_digit = False
    for i, char in enumerate(s):
        if char in '+-':
            if i > 0 and s[i-1] not in 'eE': return False
        elif char == '.':
            if met_dot or met_e: return False
            met_dot = True
        elif char in 'eE':
            if met_e or not met_digit: return False
            met_e = True
            met_digit = False
        elif char.isdigit():
            met_digit = True
        else:
            return False
    return met_digit
```

### 4. LRU Cache
**Difficulty:** Medium
**Key Technique:** OrderedDict (Apple: Clean, production-ready code)

```python
from collections import OrderedDict

class LRUCache:
    """
    Time: O(1)
    Space: O(capacity)
    """
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key: int) -> int:
        if key not in self.cache: return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache: self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
```
