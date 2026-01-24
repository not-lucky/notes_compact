# Design HashMap - Solutions

## 1. Design HashMap
(Discussed in Basics file). Implement `MyHashMap` with `put`, `get`, `remove` using separate chaining or open addressing.
O(1) Average Time, O(n) Space.

---

## 2. Design HashSet
(Discussed in Basics file). Implement `MyHashSet` with `add`, `contains`, `remove`.
O(1) Average Time, O(n) Space.

---

## 3. Two Sum
(Discussed in Two Sum Pattern file).
O(n) Time, O(n) Space.

---

## 4. LRU Cache
(Discussed in Advanced Patterns file). Implement a Least Recently Used cache.
O(1) Time for both operations, O(capacity) Space.

---

## 5. Insert Delete GetRandom O(1)
(Discussed in Advanced Patterns file). Use HashMap + Array.
O(1) Time, O(n) Space.

---

## 6. First Unique Character
(Discussed in Frequency file).
O(n) Time, O(1) Space (limited alphabet).

---

## 7. Logger Rate Limiter
Design a logger system that receives a stream of messages with their timestamps. Each unique message should only be printed at most every 10 seconds.

### Optimal Python Solution
```python
class Logger:
    def __init__(self):
        # Stores message -> next available timestamp
        self.msg_dict = {}

    def shouldPrintMessage(self, timestamp: int, message: str) -> bool:
        if message not in self.msg_dict or timestamp >= self.msg_dict[message]:
            self.msg_dict[message] = timestamp + 10
            return True
        return False
```

### Complexity Analysis
- **Time Complexity**: O(1).
- **Space Complexity**: O(M), where M is number of unique messages.
