# Solution: Interview Tips Practice Problems

## Problem: Identify bottleneck and optimize
Optimize the following O(n^2) solution:
```python
def has_pair_with_sum(arr, target):
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] + arr[j] == target:
                return True
    return False
```

### Constraints
- `n` can be up to 10^5.

### Python Implementation
```python
def has_pair_with_sum_optimized(arr: list[int], target: int) -> bool:
    """
    Time Complexity: O(n)
    Space Complexity: O(n)

    The bottleneck in the original solution was the inner loop searching for
    the complement. By using a hash set, we reduce the search to O(1).
    """
    seen = set()
    for num in arr:
        complement = target - num
        if complement in seen:
            return True
        seen.add(num)
    return False
```
