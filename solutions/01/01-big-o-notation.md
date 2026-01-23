# Big-O Notation Fundamentals

## Practice Problems

### 1. Analyze nested loop patterns
**Difficulty:** Easy
**Focus:** Basic analysis

```python
def analyze_nested_loops(n: int) -> None:
    """
    Analyzes the complexity of a basic nested loop pattern.

    Time Complexity: O(n^2) - The outer loop runs n times, and for each
                    iteration, the inner loop runs n times.
    Space Complexity: O(1) - No extra space proportional to input.
    """
    count = 0
    for i in range(n):
        for j in range(n):
            count += 1
```

### 2. Compare two approaches
**Difficulty:** Easy
**Focus:** Trade-off thinking

```python
def compare_approaches(nums: list[int], target: int) -> bool:
    """
    Compares O(n^2) brute force vs O(n) hash map approach.

    Approach 1 (Brute Force):
    Time: O(n^2)
    Space: O(1)

    Approach 2 (Hash Set):
    Time: O(n)
    Space: O(n)
    """
    # Hash set implementation (optimized for time)
    seen = set()
    for num in nums:
        if (target - num) in seen:
            return True
        seen.add(num)
    return False
```

### 3. Identify hidden complexity
**Difficulty:** Medium
**Focus:** String/list operations

```python
def hidden_complexity(chars: list[str]) -> str:
    """
    Demonstrates hidden complexity in string concatenation.

    Inefficient approach: O(n^2) due to repeated string copying.
    Efficient approach: O(n) using ''.join().
    """
    # O(n) efficient approach
    return "".join(chars)
```

### 4. Recursion tree analysis
**Difficulty:** Medium
**Focus:** Exponential vs polynomial

```python
def fibonacci(n: int) -> int:
    """
    Example of exponential time complexity through naive recursion.

    Time Complexity: O(2^n) - Each call spawns two more calls.
    Space Complexity: O(n) - Max depth of the recursion stack.
    """
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```
