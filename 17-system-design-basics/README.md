# Chapter 17: System Design Basics

This chapter bridges the gap between data structures/algorithms and system design interviews. While full system design requires understanding of distributed systems, here we focus on the **data structure choices** that appear in both coding rounds and system design discussions.

## Building Intuition

### Why System Design Questions Test Data Structures

System design questions aren't just about drawing boxes and arrows—they're fundamentally about **choosing the right data structures for the right job**. Here's the key insight:

> **Every system design decision is a data structure decision in disguise.**

When someone asks "Design a URL shortener," they're really asking "What data structure gives O(1) bidirectional lookup?" (Answer: Two hashmaps). When they ask "Design a rate limiter," they're asking "What data structure efficiently tracks time-bounded events?" (Answer: Queue/deque with timestamps).

### The Mental Model: Building Blocks

Think of system design data structures as LEGO blocks:

```
┌─────────────────────────────────────────────────────────────────┐
│                     BUILDING BLOCKS                              │
├─────────────────────────────────────────────────────────────────┤
│  HashMap     →  O(1) lookup by key (the "index")               │
│  Linked List →  O(1) reordering (the "shuffler")               │
│  Heap        →  O(1) min/max access (the "priority finder")    │
│  Queue/Deque →  O(1) ends access (the "time orderer")          │
└─────────────────────────────────────────────────────────────────┘
```

The magic happens when you **combine** these blocks. LRU Cache isn't a new data structure—it's HashMap + Doubly Linked List working together. This modular thinking is what interviewers want to see.

### Why O(1) Matters So Much

In interviews, you'll notice an obsession with O(1) operations. Here's why:

**Scale amplifies differences.** At 10 requests/second, O(1) vs O(log n) doesn't matter. At 100,000 requests/second:
- O(1) = consistent microsecond latency
- O(log n) = grows with data size, causes tail latency spikes

Real systems like Redis, Memcached, and API gateways handle millions of operations per second. Every extra operation counts.

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

```
Common O(1) building blocks:
• HashMap: O(1) lookup, insert, delete
• Doubly Linked List: O(1) insert/delete at known position
• Deque: O(1) operations at both ends
```

### 3. Eviction Strategies

| Strategy | When to Evict | Use Case |
|----------|---------------|----------|
| LRU (Least Recently Used) | Oldest access | General caching |
| LFU (Least Frequently Used) | Lowest count | Hot/cold data |
| FIFO (First In First Out) | Oldest insert | Simple queue |
| TTL (Time To Live) | Expired items | Session data |

#### Choosing the Right Eviction Strategy

**LRU (Least Recently Used):**
- Best for: General-purpose caching where recent access predicts future access
- Key insight: Temporal locality—if you accessed it recently, you'll likely access it again
- Example: Browser cache, OS page cache

**LFU (Least Frequently Used):**
- Best for: Workloads with clear "hot" and "cold" items
- Key insight: Frequency matters more than recency when popularity is stable
- Warning: Can suffer from "cache pollution" where old popular items never leave
- Example: CDN caching for viral content

**FIFO (First In First Out):**
- Best for: When insertion order is the only signal
- Key insight: Simplest to implement, no access tracking needed
- Example: Message queues, log buffers

**TTL (Time To Live):**
- Best for: Data that becomes stale after a known time
- Key insight: Time-based validity, not access-based
- Example: Session tokens, DNS cache, API response cache

## When NOT to Use These Patterns

Understanding when NOT to apply system design patterns is just as important as knowing how to implement them.

### Don't Over-Engineer Simple Requirements

```
❌ WRONG: Using LFU cache for a config store that's read once at startup
✅ RIGHT: Simple dictionary, no eviction needed

❌ WRONG: Token bucket rate limiter for a batch job that runs once daily
✅ RIGHT: No rate limiting, or simple counter if needed

❌ WRONG: Complex distributed cache for 100 key-value pairs
✅ RIGHT: In-memory dictionary, replicated to each node
```

### Anti-Patterns to Avoid

1. **Caching Write-Heavy Data**: Caches work best for read-heavy workloads. If you're updating cached data more often than reading it, you're adding complexity without benefit.

2. **Rate Limiting Everything**: Not every endpoint needs rate limiting. Internal service-to-service calls often don't need it. Focus on external APIs and expensive operations.

3. **Premature Optimization**: Don't design for 1 million requests/second when you have 100. Start simple, measure, then optimize.

4. **Ignoring Cache Invalidation**: "There are only two hard things in computer science: cache invalidation and naming things." If you can't define when cached data is stale, don't cache it.

5. **Single-Structure Thinking**: If you find yourself adding O(n) operations to maintain a property, you probably need a second data structure.

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

## Next Steps

Now that you understand how data structures apply to system design, move on to **[Chapter 18: Low-Level Design (LLD)](../18-low-level-design/)** to learn about class design and patterns, or **[Chapter 19: High-Level Design (HLD)](../19-high-level-design/)** for large-scale architecture.
