# Top-K Pattern Solutions

## 1. Kth Largest Element in an Array

Given an integer array `nums` and an integer `k`, return the kth largest element.

### Examples & Edge Cases

- **Example**: `nums = [3,2,1,5,6,4], k = 2` -> Output: 5
- **Edge Case: k = 1**: Returns the maximum.
- **Edge Case: Duplicates**: `[3,3,3], k=2` -> 3.

### Optimal Python Solution

```python
import heapq

def findKthLargest(nums: list[int], k: int) -> int:
    """
    Min-heap of size k tracks the k largest elements.
    Root is the kth largest.

    Time Complexity: O(n log k)
    Space Complexity: O(k)
    """
    # 1. Start with first k elements
    heap = nums[:k]
    heapq.heapify(heap)

    # 2. Process rest: if num > min of top-k, replace min
    for i in range(k, len(nums)):
        if nums[i] > heap[0]:
            heapq.heapreplace(heap, nums[i])

    return heap[0]
```

### Explanation

1.  **Min-Heap for K-Largest**: We want the $k$ largest elements. A min-heap allows us to efficiently find and remove the _smallest_ of these $k$ elements if we find a larger one.
2.  **Logic**: After processing all elements, the min-heap contains the $k$ largest values. The root is the minimum of these $k$, which is the $k$-th largest.

### Complexity Analysis

- **Time Complexity**: $O(n \log k)$.
- **Space Complexity**: $O(k)$.

---

## 2. Top K Frequent Elements

Given an integer array `nums` and an integer `k`, return the `k` most frequent elements.

### Examples & Edge Cases

- **Example**: `nums = [1,1,1,2,2,3], k = 2` -> `[1,2]`
- **Edge Case: Single element**: `[1], k=1` -> `[1]`.

### Optimal Python Solution

```python
import heapq
from collections import Counter

def topKFrequent(nums: list[int], k: int) -> list[int]:
    """
    Count frequencies, then use a min-heap of size k to store (freq, num).

    Time Complexity: O(n log k)
    Space Complexity: O(n)
    """
    # 1. O(n) space and time
    counts = Counter(nums)

    # 2. O(u log k) where u is number of unique elements
    # Internally uses a heap of size k
    return heapq.nlargest(k, counts.keys(), key=counts.get)
```

### Explanation

1.  **Frequency Map**: First, get the frequency of each number.
2.  **Selection**: We use `heapq.nlargest` to extract keys based on their frequency values. This is more efficient than sorting the map.

### Complexity Analysis

- **Time Complexity**: $O(n \log k)$.
- **Space Complexity**: $O(n)$.

---

## 3. K Closest Points to Origin

Given an array of `points` and an integer `k`, return the `k` closest points to `(0,0)`.

### Examples & Edge Cases

- **Example**: `points = [[1,3],[-2,2]], k = 1` -> `[[-2,2]]`
- **Edge Case: Ties**: If points are equidistant, return any.

### Optimal Python Solution

```python
import heapq

def kClosest(points: list[list[int]], k: int) -> list[list[int]]:
    """
    Use a max-heap of size k to keep the k closest points.
    We negate distances to simulate max-heap with Python's min-heap.

    Time Complexity: O(n log k)
    Space Complexity: O(k)
    """
    max_heap = []

    for x, y in points:
        # 1. Use squared distance to avoid sqrt (monotonic)
        dist = x*x + y*y

        # 2. Push negated distance
        if len(max_heap) < k:
            heapq.heappush(max_heap, (-dist, [x, y]))
        elif dist < -max_heap[0][0]:
            # If current is closer than the furthest in our k-closest
            heapq.heapreplace(max_heap, (-dist, [x, y]))

    return [p for d, p in max_heap]
```

### Explanation

1.  **Max-Heap for Closest**: We want the $k$ points with _smallest_ distances. We use a max-heap to keep track of the current $k$ candidates. The root is the _furthest_ point in our set. If a new point is closer than the root, we swap.
2.  **Optimization**: $x^2 + y^2$ is used instead of $\sqrt{x^2 + y^2}$ to save computation time.

---

## 4. Kth Largest Element in a Stream

Maintain the kth largest in a dynamic stream.

### Optimal Python Solution

```python
import heapq

class KthLargest:
    def __init__(self, k: int, nums: list[int]):
        self.k = k
        self.heap = nums
        heapq.heapify(self.heap)
        while len(self.heap) > k:
            heapq.heappop(self.heap)

    def add(self, val: int) -> int:
        heapq.heappush(self.heap, val)
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)
        return self.heap[0]
```

_(Detailed explanation omitted as it's a repeat of previous patterns)_

---

## 5. Top K Frequent Words

Return the `k` most frequent strings, sorted by frequency (high to low) and then lexicographically.

### Optimal Python Solution

```python
import heapq
from collections import Counter

class Word:
    def __init__(self, word, freq):
        self.word = word
        self.freq = freq
    def __lt__(self, other):
        # Custom comparator for Min-Heap to simulate Max-Heap behavior
        # Higher frequency is "smaller" (pops later)
        if self.freq == other.freq:
            # Lexicographically smaller is "larger" for a min-heap tie
            return self.word > other.word
        return self.freq < other.freq

def topKFrequentWords(words: list[str], k: int) -> list[str]:
    """
    Min-heap of size k with custom comparator.
    """
    counts = Counter(words)
    heap = []

    for word, freq in counts.items():
        heapq.heappush(heap, Word(word, freq))
        if len(heap) > k:
            heapq.heappop(heap)

    res = []
    while heap:
        res.append(heapq.heappop(heap).word)
    return res[::-1]
```

### Complexity Analysis

- **Time Complexity**: $O(n \log k)$.
- **Space Complexity**: $O(n)$.

---

## 6. Sort Characters By Frequency

Given a string, sort it in decreasing order based on the frequency of characters.

### Optimal Python Solution

```python
from collections import Counter
import heapq

def frequencySort(s: str) -> str:
    """
    Count chars, then use max-heap to build result.

    Time Complexity: O(n + u log u) where u is unique chars
    Space Complexity: O(n)
    """
    counts = Counter(s)
    # Max-heap of (freq, char)
    max_heap = [(-freq, char) for char, freq in counts.items()]
    heapq.heapify(max_heap)

    res = []
    while max_heap:
        freq, char = heapq.heappop(max_heap)
        res.append(char * (-freq))

    return "".join(res)
```

### Complexity Analysis

- **Time Complexity**: $O(n + u \log u)$.
- **Space Complexity**: $O(n)$.

---

## 7. K Closest Elements

Given a sorted integer array `arr`, two integers `k` and `x`, return the `k` closest integers to `x`.

### Optimal Python Solution

```python
import heapq

def findClosestElements(arr: list[int], k: int, x: int) -> list[int]:
    """
    Use a max-heap of size k based on distance from x.

    Time Complexity: O(n log k)
    Space Complexity: O(k)
    """
    # heap stores (-abs(num-x), -num)
    # We negate distance to make it a max-heap.
    # We negate num to handle the tie-break: smaller value wins.
    max_heap = []

    for num in arr:
        dist = abs(num - x)
        if len(max_heap) < k:
            heapq.heappush(max_heap, (-dist, -num))
        elif dist < -max_heap[0][0]:
            heapq.heapreplace(max_heap, (-dist, -num))

    # Extract and sort result (required by problem)
    result = [-num for dist, num in max_heap]
    return sorted(result)
```

### Complexity Analysis

- **Time Complexity**: $O(n \log k + k \log k)$.
- **Space Complexity**: $O(k)$.
