# Lessons Learned

## Complexity Analysis & Technical Accuracy
1. **Python String Concatenation (`+=`)**: When discussing space/time complexity in Python, be precise. `+=` in a loop *can* be optimized by CPython to $O(n)$ in place under certain strict conditions, but standard architectural analysis considers it $O(n^2)$ time due to memory churn and reallocation. Always recommend `.join()` for linear time.
2. **Hash Tables**: Always clarify that insertion/lookup is $O(1)$ *on average* (amortized) and $O(n)$ in the worst case (due to hash collisions). Interviewers actively test this distinction.
3. **Space Complexity and the Call Stack**: Space complexity analysis must *always* account for the recursive call stack. Do not ignore it. Time complexity like naive Fibonacci $O(2^n)$ does not mean $O(2^n)$ space; the space is bounded by the max tree depth $O(n)$.
4. **Subsets**: Generating subsets in Python using list comprehensions and concatenations is typically modeled as $O(n \cdot 2^n)$ in both time and space because each of the $2^n$ subsets takes up to $n$ elements.
5. **Python Specifics in Interviews**: Python lists are dynamic arrays (amortized $O(1)$ append), not linked lists. Python `heapq` only provides a min-heap (must negate values for max-heap). Python 3.7+ dicts maintain insertion order.

## Communication & Formatting
1. **Concrete Typed Code**: Always use modern Python type hints (e.g., `list[int]`, `Optional[TreeNode]`) in code examples to demonstrate senior-level standards.
2. **Tightest Bounds**: In interviews, while $O(n^2)$ mathematically bounds $O(n)$, interviewers want the *tightest* upper bound (Big-Theta $\Theta$).
3. **Mental Models**: Use relatable physical metaphors (desk space, scratch paper, triage) rather than abstract math when initially explaining concepts.