# Common Operation Complexities

## Practice Problems

### 1. Choose best data structure for scenario
**Difficulty:** Easy
**Focus:** Data structure selection

```python
def best_structure_scenario() -> None:
    """
    Scenario: Frequent lookups by key.
    Best choice: Dictionary (Hash Map) - O(1) average lookup.

    Scenario: Frequent insertions/deletions at both ends.
    Best choice: collections.deque - O(1) at both ends.
    """
    pass
```

### 2. Identify hidden O(n) operations
**Difficulty:** Easy
**Focus:** List/string gotchas

```python
def hidden_linear_operations(arr: list[int], target: int) -> bool:
    """
    Demonstrates hidden O(n) operations in Python.
    """
    # 'in' on a list is O(n)
    if target in arr:
        return True

    # popping from the front of a list is O(n)
    # arr.pop(0)

    return False
```

### 3. Optimize using hash table
**Difficulty:** Medium
**Focus:** Trade space for time

```python
def two_sum_optimized(nums: list[int], target: int) -> list[int]:
    """
    Optimizes Two Sum from O(n^2) to O(n) using a hash table.
    Time: O(n)
    Space: O(n)
    """
    seen = {}
    for i, num in enumerate(nums):
        diff = target - num
        if diff in seen:
            return [seen[diff], i]
        seen[num] = i
    return []
```

### 4. Compare adjacency list vs matrix
**Difficulty:** Medium
**Focus:** Graph representation

```python
def graph_representation_comparison() -> None:
    """
    Adjacency List:
    - Space: O(V + E)
    - Good for sparse graphs.

    Adjacency Matrix:
    - Space: O(V^2)
    - Good for dense graphs or checking edge existence in O(1).
    """
    pass
```

### 5. Analyze algorithm using multiple data structures
**Difficulty:** Medium
**Focus:** Combined analysis

```python
import heapq
from collections import Counter

def top_k_frequent(nums: list[int], k: int) -> list[int]:
    """
    Uses Counter (Hash Map) and Heap for combined analysis.

    1. Count frequencies: O(n) time, O(n) space
    2. Build heap: O(unique elements) time
    3. Extract k elements: O(k log unique) time

    Total Time: O(n + k log n)
    Total Space: O(n)
    """
    counts = Counter(nums)
    return heapq.nlargest(k, counts.keys(), key=counts.get)
```
