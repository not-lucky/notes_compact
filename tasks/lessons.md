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
### Chapter 3 (Hashmaps and Sets) Review Lessons
- **Variable Shadowing:** Never use built-in function names like `sum` as variable names. This causes `TypeError` when the built-in is implicitly called later or within the same scope.
- **Python Dictionary Internals:** When explaining hash tables in Python, always mention the compact dictionary implementation (Python 3.6+) and the insertion order guarantee (Python 3.7+). These are common "Senior" level interview questions.
- **Python Modulo Behavior:** Python's modulo operator (`%`) handles negative numbers differently than C++ or Java (e.g., `-1 % 5 == 4` in Python, but `-1 % 5 == -1` in C++). This is crucial for subarray sum problems involving divisibility.
- **Time Complexity Precision:** Be precise with library functions. `Counter.most_common(k)` is $O(N \log K)$, not $O(N \log N)$. Python's `list.sort()` (Timsort) uses $O(N)$ space, which affects the overall space complexity of algorithms like 3Sum/4Sum.
- **Sliding Window Logic:** When tracking matches in a sliding window (e.g., Anagram Grouping), always verify that the current character is actually part of the target pattern before updating match counts.
- **Space Complexity Distinction:** Clearly distinguish between *total space* and *auxiliary space*. Many hash map solutions require $O(N)$ auxiliary space, whereas some clever pointer/bit manipulations achieve $O(1)$ auxiliary space.
- **Null Safety in Data Structures:** When manually implementing linked structures (like Doubly Linked Lists for LRU/LFU caches), always include explicit null guards (`if node.prev:`) during pointer updates to prevent `AttributeError`.
- **Bounded Domain Optimization:** If hash keys are bounded integers (e.g., characters `a-z` or digits `0-9`), mention that a fixed-size array is faster and uses less memory than a hash map.

### Chapter 4 (Linked Lists) Review Lessons
- **Typing and Annotations:** Linked list nodes often involve recursive types or `None`. Always use `Optional[ListNode]` (or `Optional['Node']` for forward references or nodes with random pointers) to make the signature robust.
- **`Dummy Node` vs. Edge Cases:** Dummy nodes are essential for handling operations that might modify the head of a list. Emphasize that returning `dummy.next` is required because `head` might no longer be valid.
- **In-place modifications vs. Pure functions:** When an algorithm reverses or modifies a linked list in-place to achieve $O(1)$ space (e.g., checking if a list is a palindrome), it is a best practice (and often an interview requirement) to reverse it back to its original state before returning.
- **Tuples inside `heapq`:** Python heaps compare tuples element by element. When adding nodes to a heap, always include a unique tiebreaker like an explicitly incrementing `index` to prevent Python from comparing `ListNode` objects when values are equal (e.g., `(val, next_idx, node)`).
- **Reference vs. Value Equality:** When checking for list intersections, always use `is` to check for object identity, not `==` to check for value equality. Two different nodes can have the same value.
- **Edge cases:** Consistently document edge cases across linked list algorithms, specifically: empty lists (`None`), single node lists, entirely duplicate lists, and even vs. odd length considerations for fast/slow pointers.
- **Math formatting:** Use `$` signs for math formatting in markdown (e.g., $O(n)$) to ensure correct rendering.
- **Merge Lists Time Complexity:** Emphasize that adding two numbers iteratively creating a new list takes $O(\max(n, m))$ time AND $O(\max(n, m))$ auxiliary space for the result. Mentioning $O(1)$ space is acceptable only if the prompt allows modifying inputs in place, but creating a new list is standard.