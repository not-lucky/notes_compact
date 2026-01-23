# Hash Table Basics

## Practice Problems

### 1. Design HashMap (Chaining)
**Difficulty:** Easy
**Key Technique:** Array of buckets with separate chaining

```python
class MyHashMap:
    """
    Design a HashMap without using any built-in hash table libraries.

    Time: O(N/K) where N is number of keys and K is number of buckets
    Space: O(N + K)
    """
    def __init__(self):
        self.size = 1000
        self.buckets = [[] for _ in range(self.size)]

    def _hash(self, key: int) -> int:
        return key % self.size

    def put(self, key: int, value: int) -> None:
        idx = self._hash(key)
        for i, (k, v) in enumerate(self.buckets[idx]):
            if k == key:
                self.buckets[idx][i] = (key, value)
                return
        self.buckets[idx].append((key, value))

    def get(self, key: int) -> int:
        idx = self._hash(key)
        for k, v in self.buckets[idx]:
            if k == key:
                return v
        return -1

    def remove(self, key: int) -> None:
        idx = self._hash(key)
        for i, (k, v) in enumerate(self.buckets[idx]):
            if k == key:
                self.buckets[idx].pop(i)
                return
```

### 2. Design HashSet
**Difficulty:** Easy
**Key Technique:** Array of buckets

```python
class MyHashSet:
    """
    Design a HashSet without using any built-in hash table libraries.

    Time: O(N/K)
    Space: O(N + K)
    """
    def __init__(self):
        self.size = 1000
        self.buckets = [[] for _ in range(self.size)]

    def _hash(self, key: int) -> int:
        return key % self.size

    def add(self, key: int) -> None:
        if not self.contains(key):
            self.buckets[self._hash(key)].append(key)

    def remove(self, key: int) -> None:
        idx = self._hash(key)
        if key in self.buckets[idx]:
            self.buckets[idx].remove(key)

    def contains(self, key: int) -> bool:
        return key in self.buckets[self._hash(key)]
```
