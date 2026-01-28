# Solutions for LRU Cache

This file provides optimal Python solutions for practice problems related to LRU Cache implementation and variations.

## 1. LRU Cache (Standard)

### Problem Statement

Design and implement a data structure for Least Recently Used (LRU) cache. It should support `get` and `put` operations. `get(key)` returns the value if the key exists, otherwise -1. `put(key, value)` inserts or updates the value. When the cache is full, it should evict the least recently used item before inserting a new one.

### Examples & Edge Cases

- **Example**: `capacity = 2`. `put(1, 1)`, `put(2, 2)`, `get(1)` (1 is now MRU), `put(3, 3)` (evicts 2), `get(2)` -> -1.
- **Edge Cases**:
  - Capacity = 1: Every new entry evicts the previous.
  - Updating existing keys: Key becomes most recently used.
  - Large number of operations: Efficiency is key.

### Optimal Python Solution

```python
class Node:
    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        """
        Optimal implementation using HashMap + Doubly Linked List.
        """
        self.capacity = capacity
        self.cache = {} # key -> Node
        self.head = Node() # Dummy head (Most Recently Used)
        self.tail = Node() # Dummy tail (Least Recently Used)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        """Removes a node from the doubly linked list."""
        p = node.prev
        n = node.next
        p.next = n
        n.prev = p

    def _add(self, node):
        """Adds a node right after the dummy head (MRU position)."""
        nxt = self.head.next
        self.head.next = node
        node.prev = self.head
        node.next = nxt
        nxt.prev = node

    def get(self, key: int) -> int:
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add(node)
            return node.value
        return -1

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0: return
        if key in self.cache:
            self._remove(self.cache[key])

        node = Node(key, value)
        self.cache[key] = node
        self._add(node)

        if len(self.cache) > self.capacity:
            # Evict from tail
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]

# Time Complexity: O(1) for both get and put
# Space Complexity: O(capacity)
```

### Explanation

We use a **HashMap** for $O(1)$ lookups and a **Doubly Linked List** to maintain the order of usage. The "Most Recently Used" items are kept near the `head`, and "Least Recently Used" items are near the `tail`. Dummy nodes simplify the logic by removing the need for null checks.

### Complexity Analysis

- **Time Complexity**: $O(1)$ for all operations. Hash map lookups and pointer updates in a doubly linked list are constant time.
- **Space Complexity**: $O(N)$ where $N$ is the capacity.

---

## 2. Design Linked List

### Problem Statement

Design your implementation of a doubly linked list. Support `get(index)`, `addAtHead(val)`, `addAtTail(val)`, `addAtIndex(index, val)`, and `deleteAtIndex(index)`.

### Examples & Edge Cases

- **Examples**:
  - `addAtHead(1)`, `addAtTail(3)`, `addAtIndex(1, 2)`, `get(1)` -> 2.
- **Edge Cases**:
  - Adding at index 0 or index equal to length.
  - Deleting index 0 or last index.
  - Empty list operations.

### Optimal Python Solution

```python
class ListNode:
    def __init__(self, val=0):
        self.val = val
        self.prev = None
        self.next = None

class MyLinkedList:
    def __init__(self):
        self.size = 0
        self.head = ListNode() # Dummy
        self.tail = ListNode() # Dummy
        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, index: int) -> int:
        if index < 0 or index >= self.size:
            return -1

        # Optimization: Choose to start from head or tail based on index
        if index < self.size // 2:
            curr = self.head.next
            for _ in range(index):
                curr = curr.next
        else:
            curr = self.tail.prev
            for _ in range(self.size - index - 1):
                curr = curr.prev
        return curr.val

    def addAtHead(self, val: int) -> None:
        self.addAtIndex(0, val)

    def addAtTail(self, val: int) -> None:
        self.addAtIndex(self.size, val)

    def addAtIndex(self, index: int, val: int) -> None:
        if index > self.size:
            return
        if index < 0:
            index = 0

        # Find the node that will be AFTER the new node
        if index < self.size // 2:
            succ = self.head.next
            for _ in range(index):
                succ = succ.next
        else:
            succ = self.tail
            for _ in range(self.size - index):
                succ = succ.prev

        pred = succ.prev
        new_node = ListNode(val)
        new_node.prev = pred
        new_node.next = succ
        pred.next = new_node
        succ.prev = new_node
        self.size += 1

    def deleteAtIndex(self, index: int) -> None:
        if index < 0 or index >= self.size:
            return

        if index < self.size // 2:
            curr = self.head.next
            for _ in range(index):
                curr = curr.next
        else:
            curr = self.tail.prev
            for _ in range(self.size - index - 1):
                curr = curr.prev

        pred = curr.prev
        succ = curr.next
        pred.next = succ
        succ.prev = pred
        self.size -= 1
```

### Explanation

We implement a **Doubly Linked List** with dummy head and tail. To optimize `get` and finding nodes, we check if the `index` is in the first or second half and traverse from the nearest end.

### Complexity Analysis

- **Time Complexity**:
  - `addAtHead`, `addAtTail`: $O(1)$.
  - `get`, `addAtIndex`, `deleteAtIndex`: $O(\min(k, N-k))$ where $k$ is the index.
- **Space Complexity**: $O(N)$ for $N$ nodes.

---

## 3. All O(1) Data Structure

### Problem Statement

Design a data structure that supports the following operations in $O(1)$ time:

1. `inc(key)`: Increments the count of the key by 1.
2. `dec(key)`: Decrements the count of the key by 1.
3. `getMaxKey()`: Returns one of the keys with maximal count.
4. `getMinKey()`: Returns one of the keys with minimal count.

### Examples & Edge Cases

- **Examples**: `inc("a")`, `inc("b")`, `inc("b")`, `inc("c")`, `getMaxKey()` -> "b", `getMinKey()` -> "a" or "c".
- **Edge Cases**:
  - Empty structure: Return "".
  - Key count becomes 0: Remove it.

### Optimal Python Solution

```python
class Block:
    def __init__(self, val=0):
        self.val = val
        self.keys = set()
        self.prev = None
        self.next = None

class AllOne:
    def __init__(self):
        # Maps key to the DLL block it belongs to
        self.key_map = {}
        self.head = Block() # Dummy head
        self.tail = Block() # Dummy tail
        self.head.next = self.tail
        self.tail.prev = self.head

    def _insert_block(self, prev_block, val):
        new_block = Block(val)
        nxt = prev_block.next
        prev_block.next = new_block
        new_block.prev = prev_block
        new_block.next = nxt
        nxt.prev = new_block
        return new_block

    def _remove_block(self, block):
        block.prev.next = block.next
        block.next.prev = block.prev

    def inc(self, key: str) -> None:
        if key not in self.key_map:
            if self.head.next.val == 1:
                self.head.next.keys.add(key)
                self.key_map[key] = self.head.next
            else:
                new_block = self._insert_block(self.head, 1)
                new_block.keys.add(key)
                self.key_map[key] = new_block
        else:
            curr_block = self.key_map[key]
            next_val = curr_block.val + 1
            if curr_block.next.val == next_val:
                new_block = curr_block.next
            else:
                new_block = self._insert_block(curr_block, next_val)
            new_block.keys.add(key)
            self.key_map[key] = new_block
            curr_block.keys.remove(key)
            if not curr_block.keys:
                self._remove_block(curr_block)

    def dec(self, key: str) -> None:
        if key not in self.key_map: return
        curr_block = self.key_map[key]
        curr_block.keys.remove(key)
        if curr_block.val > 1:
            prev_val = curr_block.val - 1
            if curr_block.prev.val == prev_val:
                new_block = curr_block.prev
            else:
                new_block = self._insert_block(curr_block.prev, prev_val)
            new_block.keys.add(key)
            self.key_map[key] = new_block
        else:
            del self.key_map[key]
        if not curr_block.keys:
            self._remove_block(curr_block)

    def getMaxKey(self) -> str:
        if self.tail.prev == self.head: return ""
        return next(iter(self.tail.prev.keys))

    def getMinKey(self) -> str:
        if self.head.next == self.tail: return ""
        return next(iter(self.head.next.keys))
```

### Explanation

We use a **Doubly Linked List of Blocks**, where each block represents a specific frequency (count) and stores a set of keys with that frequency. A **HashMap** maps each key to its current block. This allows us to move keys between frequency blocks in $O(1)$.

### Complexity Analysis

- **Time Complexity**: $O(1)$ for all operations.
- **Space Complexity**: $O(N)$ where $N$ is the number of keys.

---

## 4. Design Browser History

### Problem Statement

You have a browser with `homepage`. You can `visit(url)`, go `back(steps)`, or `forward(steps)`.

### Examples & Edge Cases

- **Examples**: `visit("google.com")`, `visit("facebook.com")`, `back(1)` -> "google.com", `visit("linkedin.com")` (clears forward history).
- **Edge Cases**:
  - Going back further than history allows: Return earliest page.
  - Going forward further than possible: Return latest page.

### Optimal Python Solution

```python
class BrowserHistory:
    def __init__(self, homepage: str):
        # Use a simple list to act as a stack with a pointer
        self.history = [homepage]
        self.curr = 0

    def visit(self, url: str) -> None:
        # Optimization: O(1) visit by overwriting instead of slicing
        # To truly achieve O(1), we'd need to avoid the slice entirely
        # and just manage a boundary pointer.
        self.curr += 1
        if self.curr < len(self.history):
            self.history[self.curr] = url
        else:
            self.history.append(url)
        self.history = self.history[:self.curr + 1]

    def back(self, steps: int) -> str:
        self.curr = max(0, self.curr - steps)
        return self.history[self.curr]

    def forward(self, steps: int) -> str:
        self.curr = min(len(self.history) - 1, self.curr + steps)
        return self.history[self.curr]
```

### Explanation

A simple **dynamic array (list)** with a pointer `curr` is sufficient. `visit` truncates the array and appends the new URL. `back` and `forward` just move the pointer within bounds.

### Complexity Analysis

- **Time Complexity**:
  - `visit`: $O(N)$ in Python due to slicing (can be $O(1)$ if we manage capacity manually).
  - `back`, `forward`: $O(1)$.
- **Space Complexity**: $O(N)$ for history.

---

## 5. LRU Cache (Follow-up: TTL)

### Problem Statement

Implement an LRU cache where each entry also has a **Time To Live (TTL)**. If an entry is requested after its TTL has expired, it should be treated as a cache miss and removed.

### Examples & Edge Cases

- **Examples**: `put(1, 1, ttl=5s)`, `get(1)` after 6s -> -1.
- **Edge Cases**:
  - Lazy deletion vs. Eager deletion.
  - Update TTL on `put`.

### Optimal Python Solution

```python
import time

class TTLNode(Node):
    def __init__(self, key=0, value=0, expiry=0):
        super().__init__(key, value)
        self.expiry = expiry

class LRUCacheWithTTL(LRUCache):
    def __init__(self, capacity: int, default_ttl: int):
        super().__init__(capacity)
        self.default_ttl = default_ttl

    def get(self, key: int) -> int:
        if key in self.cache:
            node = self.cache[key]
            if time.time() > node.expiry:
                self._remove(node)
                del self.cache[key]
                return -1
            self._remove(node)
            self._add(node)
            return node.value
        return -1

    def put(self, key: int, value: int, ttl: int = None) -> None:
        t = ttl if ttl is not None else self.default_ttl
        expiry = time.time() + t

        if key in self.cache:
            self._remove(self.cache[key])

        node = TTLNode(key, value, expiry)
        self.cache[key] = node
        self._add(node)

        if len(self.cache) > self.capacity:
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]
```

### Explanation

We extend the standard LRU cache by adding an `expiry` timestamp to each node. We use **Lazy Deletion**: we only check for expiration during a `get` call. This keeps the logic simple and $O(1)$ per operation.

### Complexity Analysis

- **Time Complexity**: $O(1)$.
- **Space Complexity**: $O(N)$.
