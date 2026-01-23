# Solution: Hash Table Basics

## Problem Statement
The goal is to understand and implement a basic hash table (HashMap) with common operations such as insertion, retrieval, and deletion.

## Constraints
- Handle collisions using a simple technique (e.g., Chaining).
- Provide basic operations: `put`, `get`, and `remove`.
- Keys and values are integers for simplicity.

## Example (Input/Output)
```python
hash_map = MyHashMap()
hash_map.put(1, 1)
hash_map.put(2, 2)
hash_map.get(1)            # returns 1
hash_map.get(3)            # returns -1 (not found)
hash_map.put(2, 1)         # update the existing value
hash_map.get(2)            # returns 1
hash_map.remove(2)         # remove the mapping for 2
hash_map.get(2)            # returns -1 (not found)
```

## Python Implementation
```python
class MyHashMap:
    """
    Design a HashMap without using any built-in hash table libraries.

    Implementation: Chaining with list of tuples.
    """
    def __init__(self):
        self.size = 1000
        self.buckets = [[] for _ in range(self.size)]

    def _hash(self, key: int) -> int:
        return key % self.size

    def put(self, key: int, value: int) -> None:
        idx = self._hash(key)
        bucket = self.buckets[idx]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))

    def get(self, key: int) -> int:
        idx = self._hash(key)
        bucket = self.buckets[idx]
        for k, v in bucket:
            if k == key:
                return v
        return -1

    def remove(self, key: int) -> None:
        idx = self._hash(key)
        bucket = self.buckets[idx]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                return
```
