"""
01-data-structure-choices.py

Practice problems for Data Structure Choices in System Design.
"""

from collections import Counter, OrderedDict
import heapq
import time
from typing import List, Any

# 1. Two Sum (HashMap practice)
def two_sum(nums: List[int], target: int) -> List[int]:
    """O(1) lookup by using complement as key."""
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

# 2. Top K Frequent Elements (HashMap + Heap practice)
def top_k_frequent(nums: List[int], k: int) -> List[int]:
    """O(N log K) using Counter and Min-Heap."""
    count = Counter(nums)
    return heapq.nlargest(k, count.keys(), key=count.get)

# 3. Time Based Key-Value Store (Conceptual Practice)
class TimeMap:
    """
    HashMap: key -> list of (timestamp, value)
    Binary Search: O(log N) to find floor timestamp.
    """
    def __init__(self):
        self.store = {}

    def set(self, key: str, value: str, timestamp: int) -> None:
        if key not in self.store:
            self.store[key] = []
        self.store[key].append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        if key not in self.store:
            return ""

        values = self.store[key]
        # Binary search for the rightmost timestamp <= given timestamp
        import bisect
        idx = bisect.bisect_right(values, (timestamp, chr(127)))

        if idx == 0:
            return ""
        return values[idx-1][1]

# 4. Running Median (Two Heaps practice)
class MedianFinder:
    """
    small (max-heap): stores the smaller half
    large (min-heap): stores the larger half
    O(log N) add, O(1) find.
    """
    def __init__(self):
        self.small = []  # Max-heap (invert values)
        self.large = []  # Min-heap

    def add_num(self, num: int) -> None:
        heapq.heappush(self.small, -num)
        # Ensure every num in small <= every num in large
        if self.small and self.large and (-self.small[0] > self.large[0]):
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)

        # Balance sizes
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        if len(self.large) > len(self.small) + 1:
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)

    def find_median(self) -> float:
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        elif len(self.large) > len(self.small):
            return float(self.large[0])
        return (-self.small[0] + self.large[0]) / 2.0

# 5. Simple TTL Cache
class TTLCache:
    def __init__(self, ttl_seconds: int):
        self.ttl = ttl_seconds
        self.cache = {}

    def get(self, key: Any) -> Any:
        if key in self.cache:
            val, expiry = self.cache[key]
            if time.time() < expiry:
                return val
            del self.cache[key]
        return None

    def put(self, key: Any, value: Any) -> None:
        self.cache[key] = (value, time.time() + self.ttl)
