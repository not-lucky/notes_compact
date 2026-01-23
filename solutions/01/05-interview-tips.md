# How to Discuss Complexity in Interviews

## Practice Problems

### 1. Explain complexity of your own code
**Difficulty:** Easy
**Focus:** Communication

```python
def explain_complexity() -> None:
    """
    Best practice for explaining complexity:
    "The time complexity is O(n) because we iterate through the list once.
    The space complexity is O(1) as we only store a few variables regardless
    of the input size."
    """
    pass
```

### 2. Identify bottleneck and optimize
**Difficulty:** Medium
**Focus:** Optimization

```python
def optimize_bottleneck(nums: list[int]) -> list[int]:
    """
    Scenario: O(n^2) due to nested linear search.
    Optimization: Use a set for O(1) lookups to reach O(n).
    """
    seen = set()
    res = []
    for num in nums:
        if num not in seen: # O(1) average
            res.append(num)
            seen.add(num)
    return res
```

### 3. Compare two approaches with trade-offs
**Difficulty:** Medium
**Focus:** Trade-off discussion

```python
def trade_off_discussion() -> None:
    """
    Discussing trade-offs:
    "We can use a two-pointer approach for O(1) space if the input is sorted,
    otherwise we use a hash map for O(n) space to maintain O(n) time."
    """
    pass
```

### 4. Prove why complexity can't be improved
**Difficulty:** Hard
**Focus:** Lower bounds

```python
def lower_bound_proof() -> None:
    """
    Example: Any comparison-based sorting algorithm must be at least O(n log n).
    Reasoning: There are n! possible permutations, and each comparison
    halves the remaining search space. log2(n!) is roughly n log n.
    """
    pass
```

### 5. Mock interview with complexity questions
**Difficulty:** Medium
**Focus:** Full practice

```python
def mock_interview_prep() -> None:
    """
    Checklist:
    - State BOTH time and space complexity.
    - Identify the bottleneck upfront.
    - Be ready to discuss space-time trade-offs.
    - Don't forget the recursion call stack space.
    """
    pass
```
