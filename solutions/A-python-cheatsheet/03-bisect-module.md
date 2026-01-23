# Bisect Module

## Practice Problems

### 1. Search Insert Position
**Difficulty:** Easy
**Key Technique:** bisect_left

```python
import bisect

def search_insert(nums: list[int], target: int) -> int:
    """
    Time: O(log n)
    Space: O(1)
    """
    return bisect.bisect_left(nums, target)
```

### 2. Find First and Last Position of Element in Sorted Array
**Difficulty:** Medium
**Key Technique:** bisect_left + bisect_right

```python
import bisect

def search_range(nums: list[int], target: int) -> list[int]:
    """
    Time: O(log n)
    Space: O(1)
    """
    l = bisect.bisect_left(nums, target)
    if l == len(nums) or nums[l] != target:
        return [-1, -1]
    r = bisect.bisect_right(nums, target) - 1
    return [l, r]
```

### 3. Time Based Key-Value Store
**Difficulty:** Medium
**Key Technique:** bisect_right for floor

```python
import bisect

class TimeMap:
    """
    Time: O(log n) for get, O(1) for set
    Space: O(n)
    """
    def __init__(self):
        self.store = {} # key -> (list of timestamps, list of values)

    def set(self, key: str, value: str, timestamp: int) -> None:
        if key not in self.store:
            self.store[key] = ([], [])
        self.store[key][0].append(timestamp)
        self.store[key][1].append(value)

    def get(self, key: str, timestamp: int) -> str:
        if key not in self.store:
            return ""
        times, values = self.store[key]
        idx = bisect.bisect_right(times, timestamp) - 1
        return values[idx] if idx >= 0 else ""
```

### 4. Count of Smaller Numbers After Self
**Difficulty:** Hard
**Key Technique:** bisect + sorted list maintenance

```python
import bisect

def count_smaller(nums: list[int]) -> list[int]:
    """
    Time: O(n^2) - bisect is log n but insert is O(n)
    Space: O(n)
    """
    res = []
    sorted_nums = []
    for n in reversed(nums):
        idx = bisect.bisect_left(sorted_nums, n)
        res.append(idx)
        bisect.insort(sorted_nums, n)
    return res[::-1]
```
