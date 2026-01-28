# Solutions for Data Structure Choices for System Design

This file provides optimal Python solutions for the practice problems related to choosing data structures in system design.

## 1. Design HashMap

### Problem Statement

Design a HashMap without using any built-in hash table libraries. You should implement basic operations: `put(key, value)`, `get(key)`, and `remove(key)`.

### Examples & Edge Cases

- **Examples**:
  - `put(1, 1)`, `put(2, 2)`, `get(1)` -> 1, `get(3)` -> -1, `put(2, 1)`, `get(2)` -> 1, `remove(2)`, `get(2)` -> -1.
- **Edge Cases**:
  - **Collisions**: Multiple keys hashing to the same bucket.
  - **Large number of keys**: Efficient distribution.
  - **Updating existing keys**: Replacing the value.

### Optimal Python Solution

```python
class MyHashMap:
    def __init__(self):
        # Use a prime number for the number of buckets to reduce collisions
        self.size = 1999
        self.table = [[] for _ in range(self.size)]

    def _hash(self, key):
        # Basic modulo hashing
        return key % self.size

    def put(self, key: int, value: int) -> None:
        """
        Inserts a (key, value) pair into the HashMap.
        If the key already exists, update the corresponding value.
        """
        hash_key = self._hash(key)
        for i, (k, v) in enumerate(self.table[hash_key]):
            if k == key:
                self.table[hash_key][i] = (key, value)
                return
        self.table[hash_key].append((key, value))

    def get(self, key: int) -> int:
        """
        Returns the value to which the specified key is mapped,
        or -1 if this map contains no mapping for the key.
        """
        hash_key = self._hash(key)
        for k, v in self.table[hash_key]:
            if k == key:
                return v
        return -1

    def remove(self, key: int) -> None:
        """
        Removes the mapping for the specific key if this map contains the mapping for the key.
        """
        hash_key = self._hash(key)
        for i, (k, v) in enumerate(self.table[hash_key]):
            if k == key:
                self.table[hash_key].pop(i)
                return
```

### Explanation

The implementation uses **Chaining** for collision handling. We maintain an array of buckets, where each bucket contains a list of key-value pairs.

1. `_hash`: Computes the index in the bucket array using the modulo operator.
2. `put`: Finds the bucket, checks if the key exists to update, otherwise appends.
3. `get`: Finds the bucket and searches for the key.
4. `remove`: Finds the bucket and removes the key-value pair if it exists.

### Complexity Analysis

- **Time Complexity**:
  - `put`, `get`, `remove`: Average $O(1)$, Worst-case $O(N/K)$ where $N$ is total keys and $K$ is number of buckets.
- **Space Complexity**: $O(K + N)$ where $K$ is the number of predefined buckets and $N$ is the number of keys stored.

---

## 2. LRU Cache

### Problem Statement

Design a data structure that follows the constraints of a **Least Recently Used (LRU) cache**. Implement `get(key)` and `put(key, value)`. Both operations must run in $O(1)$ time complexity.

### Examples & Edge Cases

- **Examples**:
  - `LRUCache(2)`, `put(1, 1)`, `put(2, 2)`, `get(1)` (1 becomes MRU), `put(3, 3)` (evicts 2), `get(2)` -> -1.
- **Edge Cases**:
  - **Capacity 1**: Evicts on every new put.
  - **Updating existing key**: Moves it to the front without evicting.
  - **Get of missing key**: Returns -1.

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
        self.capacity = capacity
        self.cache = {} # key -> Node
        # Dummy nodes to simplify addition/removal logic
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        # Standard DLL node removal
        prev, nxt = node.prev, node.next
        prev.next, nxt.prev = nxt, prev

    def _add_to_head(self, node):
        # Add node right after dummy head
        nxt = self.head.next
        self.head.next = node
        node.prev = self.head
        node.next = nxt
        nxt.prev = node

    def get(self, key: int) -> int:
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add_to_head(node)
            return node.value
        return -1

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0: return
        if key in self.cache:
            self._remove(self.cache[key])

        node = Node(key, value)
        self.cache[key] = node
        self._add_to_head(node)

        if len(self.cache) > self.capacity:
            # Evict LRU (node before tail)
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]
```

### Explanation

We combine a **HashMap** and a **Doubly Linked List (DLL)**.

1. The HashMap provides $O(1)$ access to the nodes by key.
2. The DLL allows $O(1)$ removal and re-insertion at the head (Most Recently Used).
3. Dummy head and tail nodes eliminate edge case checks for empty lists or single elements.

### Complexity Analysis

- **Time Complexity**: $O(1)$ for both `get` and `put` because hash lookups and pointer updates are constant time operations.
- **Space Complexity**: $O(\text{capacity})$ to store the keys in the hash map and nodes in the DLL.

---

## 3. Time Based Key-Value Store

### Problem Statement

Design a time-based key-value data structure that can store multiple values for the same key at different timestamps and retrieve the key's value at a certain timestamp.

### Examples & Edge Cases

- **Examples**:
  - `set("foo", "bar", 1)`, `get("foo", 1)` -> "bar", `get("foo", 3)` -> "bar" (finds latest before 3), `set("foo", "bar2", 4)`, `get("foo", 4)` -> "bar2".
- **Edge Cases**:
  - **Timestamp before any entry**: Return empty string.
  - **Multiple values for same key**: Must return the one with `timestamp_prev <= timestamp_query`.

### Optimal Python Solution

```python
import bisect

class TimeMap:
    def __init__(self):
        # key -> list of [timestamp, value]
        self.store = {}

    def set(self, key: str, value: str, timestamp: int) -> None:
        if key not in self.store:
            self.store[key] = []
        # Timestamps are strictly increasing as per constraints
        self.store[key].append([timestamp, value])

    def get(self, key: str, timestamp: int) -> str:
        if key not in self.store:
            return ""

        history = self.store[key]
        # Binary search for the right position
        # history is naturally sorted by timestamp.
        # We use [timestamp, chr(127)] as a hack to ensure we find the rightmost
        # index for the given timestamp in the list of [timestamp, value] pairs.
        idx = bisect.bisect_right(history, [timestamp, chr(127)])

        if idx == 0:
            return ""
        return history[idx-1][1]
```

### Explanation

1. We use a **HashMap** where the key is the string and the value is a **Sorted List** of `[timestamp, value]` pairs.
2. Since timestamps are added in strictly increasing order, the list stays sorted.
3. For `get`, we use **Binary Search** (`bisect_right`) to find the largest timestamp $\leq$ target in $O(\log N)$ time.

### Complexity Analysis

- **Time Complexity**:
  - `set`: $O(1)$ for appending to list.
  - `get`: $O(\log N)$ where $N$ is the number of timestamps for a given key.
- **Space Complexity**: $O(M \times N)$ where $M$ is the number of keys and $N$ is the number of values per key.

---

## 4. Find Median from Data Stream

### Problem Statement

Design a data structure that supports adding integers from a stream and finding the median of all elements added so far.

### Examples & Edge Cases

- **Examples**:
  - `addNum(1)`, `addNum(2)`, `findMedian()` -> 1.5, `addNum(3)`, `findMedian()` -> 2.0.
- **Edge Cases**:
  - **Empty stream**: Not typically handled, assume at least one call.
  - **Duplicate numbers**: Heaps handle these naturally.
  - **Even vs. Odd count**: Mean of middle two vs. middle element.

### Optimal Python Solution

```python
import heapq

class MedianFinder:
    def __init__(self):
        # Max-heap for the smaller half (using negative values)
        self.small = []
        # Min-heap for the larger half
        self.large = []

    def addNum(self, num: int) -> None:
        # Step 1: Push to small heap, then move max of small to large
        heapq.heappush(self.small, -num)
        heapq.heappush(self.large, -heapq.heappop(self.small))

        # Step 2: Keep small heap size >= large heap size
        if len(self.large) > len(self.small):
            heapq.heappush(self.small, -heapq.heappop(self.large))

    def findMedian(self) -> float:
        if len(self.small) > len(self.large):
            return -self.small[0]
        return (-self.small[0] + self.large[0]) / 2.0
```

### Explanation

We use **Two Heaps** to maintain the stream split in the middle.

1. `small` (Max-heap): Stores the smaller half of numbers.
2. `large` (Min-heap): Stores the larger half of numbers.
3. Balancing ensures the median is either the top of `small` (if odd total) or the average of the tops of both (if even total).

### Complexity Analysis

- **Time Complexity**:
  - `addNum`: $O(\log N)$ for heap operations.
  - `findMedian`: $O(1)$ as we only look at the top of the heaps.
- **Space Complexity**: $O(N)$ to store all numbers.

---

## 5. Design Twitter

### Problem Statement

Design a simplified version of Twitter where users can post tweets, follow/unfollow others, and see the 10 most recent tweets in their feed.

### Examples & Edge Cases

- **Examples**:
  - `postTweet(1, 5)`, `getNewsFeed(1)` -> [5], `follow(1, 2)`, `postTweet(2, 6)`, `getNewsFeed(1)` -> [6, 5], `unfollow(1, 2)`, `getNewsFeed(1)` -> [5].
- **Edge Cases**:
  - **Self-following**: Not usually counted.
  - **No tweets**: Return empty list.
  - **Users with >10 tweets**: Only show the latest 10.

### Optimal Python Solution

```python
import heapq
from collections import defaultdict

class Twitter:
    def __init__(self):
        self.timestamp = 0
        self.user_tweets = defaultdict(list) # userId -> list of (time, tweetId)
        self.following = defaultdict(set)    # userId -> set of followeeId

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.timestamp -= 1 # Using negative for min-heap as max-heap
        self.user_tweets[userId].append((self.timestamp, tweetId))

    def getNewsFeed(self, userId: int) -> list[int]:
        res = []
        min_heap = []

        # Add the user to their own "following" set conceptually
        users = self.following[userId] | {userId}

        for u in users:
            if u in self.user_tweets:
                # Add the most recent tweet of each followee to the heap
                last_idx = len(self.user_tweets[u]) - 1
                time, tweetId = self.user_tweets[u][last_idx]
                heapq.heappush(min_heap, (time, tweetId, u, last_idx - 1))

        while min_heap and len(res) < 10:
            time, tweetId, u, idx = heapq.heappop(min_heap)
            res.append(tweetId)
            if idx >= 0:
                next_time, next_tweetId = self.user_tweets[u][idx]
                heapq.heappush(min_heap, (next_time, next_tweetId, u, idx - 1))
        return res

    def follow(self, followerId: int, followeeId: int) -> None:
        if followerId != followeeId:
            self.following[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        self.following[followerId].discard(followeeId)
```

### Explanation

1. **Data Structures**: `defaultdict(list)` for tweets and `defaultdict(set)` for followers.
2. **Merging Feeds**: `getNewsFeed` uses a **Min-Heap** (acting as a Max-Heap with negative timestamps) to perform a **K-way Merge** of the tweet lists from all followees.
3. We only pull the latest 10 tweets, making it efficient even if a user follows many people.

### Complexity Analysis

- **Time Complexity**:
  - `postTweet`, `follow`, `unfollow`: $O(1)$.
  - `getNewsFeed`: $O(F \log F)$ where $F$ is the number of followees (heap size), capped by the 10 iterations.
- **Space Complexity**: $O(U + T)$ where $U$ is total users/relationships and $T$ is total tweets.

---

## 6. Stock Price Fluctuation

### Problem Statement

Design a system to track a stock's price over time. You should be able to update the price at a specific timestamp and retrieve the `latest`, `maximum`, `minimum`, and `current` prices.

### Examples & Edge Cases

- **Examples**:
  - `update(1, 10)`, `update(2, 5)`, `current()` -> 5, `maximum()` -> 10, `update(1, 3)`, `maximum()` -> 5, `minimum()` -> 3.
- **Edge Cases**:
  - **Price corrections**: `update` can change a previous timestamp's price.
  - **Latest timestamp**: Not necessarily the one most recently updated.

### Optimal Python Solution

```python
import heapq

class StockPrice:
    def __init__(self):
        self.timestamps = {} # timestamp -> price
        self.max_time = 0
        self.min_heap = []   # (price, timestamp)
        self.max_heap = []   # (-price, timestamp)

    def update(self, timestamp: int, price: int) -> None:
        self.timestamps[timestamp] = price
        self.max_time = max(self.max_time, timestamp)
        heapq.heappush(self.min_heap, (price, timestamp))
        heapq.heappush(self.max_heap, (-price, timestamp))

    def current(self) -> int:
        return self.timestamps[self.max_time]

    def maximum(self) -> int:
        while True:
            price, ts = self.max_heap[0]
            if -price == self.timestamps[ts]:
                return -price
            heapq.heappop(self.max_heap) # Stale price

    def minimum(self) -> int:
        while True:
            price, ts = self.min_heap[0]
            if price == self.timestamps[ts]:
                return price
            heapq.heappop(self.min_heap) # Stale price
```

### Explanation

1. **HashMap**: Stores the definitive `timestamp -> price` mapping.
2. **Two Heaps**: Track the global min and max prices.
3. **Lazy Deletion**: Since `update` can change old prices, the heaps might contain "stale" entries. When querying `minimum` or `maximum`, we pop the top of the heap until we find an entry that matches the current value in our HashMap.

### Complexity Analysis

- **Time Complexity**:
  - `update`: $O(\log N)$ to push to heaps.
  - `current`: $O(1)$.
  - `maximum`/`minimum`: $O(\log N)$ amortized (to clear stale entries).
- **Space Complexity**: $O(N)$ where $N$ is the number of updates.
