# Chapter 17: System Design Basics

This chapter bridges the gap between data structures/algorithms and system design interviews. While full system design requires understanding of distributed systems, here we focus on the **data structure choices** that appear in both coding rounds and system design discussions.

## Why This Matters for Interviews

1. **Hybrid questions**: "Design an LRU cache" is both a coding and design question
2. **Trade-off discussions**: Interviewers want to hear you reason about choices
3. **Follow-up questions**: "How would this scale?" after coding solutions
4. **System design warm-up**: Shows you can think beyond just algorithms

---

## Core Topics

| Topic | Interview Relevance | Example Questions |
|-------|-------------------|-------------------|
| Data Structure Choices | Trade-off discussions | "Why HashMap over TreeMap?" |
| LRU Cache | Very common coding question | "Implement LRU with O(1) operations" |
| LFU Cache | Advanced cache question | "Implement LFU cache" |
| Rate Limiter | System design staple | "Design API rate limiting" |

---

## When These Topics Appear

### Coding Interviews
- **LRU Cache**: Frequently asked at Google, Meta, Amazon
- **LFU Cache**: Asked at top-tier companies for senior roles
- **Rate Limiter**: Sliding window, token bucket implementations

### System Design Interviews
- **Cache Design**: Eviction policies, distributed caching
- **Rate Limiting**: API gateways, DDoS protection
- **Data Store Selection**: When to use Redis vs DynamoDB vs PostgreSQL

---

## Chapter Contents

| # | Topic | Key Concepts |
|---|-------|--------------|
| 01 | [Data Structure Choices](./01-data-structure-choices.md) | Trade-offs: HashMap vs Tree vs Heap |
| 02 | [LRU Cache](./02-lru-cache.md) | OrderedDict, doubly linked list + hashmap |
| 03 | [LFU Cache](./03-lfu-cache.md) | Frequency buckets, O(1) operations |
| 04 | [Rate Limiter](./04-rate-limiter.md) | Token bucket, sliding window, leaky bucket |

---

## Key Patterns

### 1. Combining Data Structures

Most system design data structure problems require **combining** structures:

```
LRU Cache = HashMap + Doubly Linked List
LFU Cache = HashMap + Frequency Map + Doubly Linked Lists
Rate Limiter = Queue/Deque + Counter or HashMap
```

### 2. O(1) Requirement

System design problems often require O(1) for core operations:

```python
# Common O(1) building blocks:
- HashMap: O(1) lookup, insert, delete
- Doubly Linked List: O(1) insert/delete at known position
- Deque: O(1) operations at both ends
```

### 3. Eviction Strategies

| Strategy | When to Evict | Use Case |
|----------|---------------|----------|
| LRU (Least Recently Used) | Oldest access | General caching |
| LFU (Least Frequently Used) | Lowest count | Hot/cold data |
| FIFO (First In First Out) | Oldest insert | Simple queue |
| TTL (Time To Live) | Expired items | Session data |

---

## Implementation Template: Generic Cache

```python
from abc import ABC, abstractmethod
from typing import TypeVar, Generic

K = TypeVar('K')
V = TypeVar('V')

class Cache(ABC, Generic[K, V]):
    """
    Abstract base class for cache implementations.
    All operations should be O(1).
    """

    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self.capacity = capacity

    @abstractmethod
    def get(self, key: K) -> V | None:
        """Retrieve value and update access metadata."""
        pass

    @abstractmethod
    def put(self, key: K, value: V) -> None:
        """Insert/update value, evict if necessary."""
        pass

    @abstractmethod
    def __len__(self) -> int:
        """Return current number of items."""
        pass
```

---

## Common Mistakes

1. **Forgetting edge cases**: Capacity 0 or 1, duplicate keys
2. **Not maintaining order**: LRU must track access order correctly
3. **Wrong complexity**: Using list.remove() makes it O(n)
4. **Thread safety**: Production caches need locks (usually not in interviews)
5. **Ignoring capacity**: Not evicting when full

---

## Time Complexity Goals

| Operation | Target | Structure to Use |
|-----------|--------|-----------------|
| Get | O(1) | HashMap for lookup |
| Put | O(1) | HashMap + linked list |
| Evict | O(1) | Maintain eviction candidate |
| Update access | O(1) | Doubly linked list |

---

## Interview Tips

1. **Start with the interface**: Define `get()` and `put()` first
2. **Explain trade-offs**: "I'm using a HashMap for O(1) lookup..."
3. **Draw the structure**: Visualize node connections
4. **Handle edge cases explicitly**: Empty cache, single item, updates
5. **Mention production concerns**: Thread safety, persistence, distribution

---

## Connection to Full System Design

| Coding Problem | System Design Extension |
|----------------|------------------------|
| LRU Cache | Distributed cache with Redis, Memcached |
| Rate Limiter | API Gateway, load balancer integration |
| Data structure choice | Database selection, indexing strategies |

---

## Classic Problems by Company

| Company | Favorite Problems |
|---------|------------------|
| Google | LRU Cache, Design HashMap, Design Hit Counter |
| Meta | LRU Cache, LFU Cache, Design Twitter Feed |
| Amazon | LRU Cache, Design Rate Limiter, Time-Based Key-Value Store |
| Microsoft | LRU Cache, Design In-Memory File System |
| Apple | Design Data Structure (multiple ops O(1)) |

---

## Start: [01-data-structure-choices.md](./01-data-structure-choices.md)

Begin with understanding when to choose different data structures for system design scenarios.
