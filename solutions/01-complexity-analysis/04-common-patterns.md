# Solution: Common Operation Complexities

## Problem: Choose best data structure for scenario
Given a stream of integers, find if a target value has been seen before.

### Constraints
- Stream can have millions of integers.
- Quick lookup is required.

### Python Implementation
```python
class SeenTracker:
    def __init__(self):
        self.seen = set()

    def add_and_check(self, val: int) -> bool:
        """
        Time Complexity: O(1) average for add and check
        Space Complexity: O(n) where n is the number of unique elements seen
        """
        if val in self.seen:
            return True
        self.seen.add(val)
        return False
```
