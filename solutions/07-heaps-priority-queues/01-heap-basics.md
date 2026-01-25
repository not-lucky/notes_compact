# Heap Basics Solutions

## 1. Last Stone Weight
You are given an array of integers `stones` where `stones[i]` is the weight of the ith stone.
We are playing a game with the stones. On each turn, we choose the heaviest two stones and smash them together. Suppose the heaviest two stones have weights `x` and `y` with `x <= y`. The result of this smash is:
- If `x == y`, both stones are destroyed.
- If `x != y`, the stone of weight `x` is destroyed, and the stone of weight `y` has new weight `y - x`.
At the end of the game, there is at most one stone left. Return the weight of the last remaining stone. If there are no stones left, return 0.

### Examples & Edge Cases
- **Example 1**: `stones = [2,7,4,1,8,1]` -> Output: 1
    - Smash 7 and 8, get 1. Stones: `[2,4,1,1,1]`
    - Smash 2 and 4, get 2. Stones: `[2,1,1,1]`
    - Smash 2 and 1, get 1. Stones: `[1,1,1]`
    - Smash 1 and 1, get 0. Stones: `[1]`
    - Final stone is 1.
- **Edge Case: Empty list**: Should return 0.
- **Edge Case: One stone**: Returns that stone's weight.
- **Edge Case: All same weights**: May result in 0 or a single stone depending on parity.

### Optimal Python Solution
```python
import heapq

def lastStoneWeight(stones: list[int]) -> int:
    """
    Use a Max Heap to always extract the two heaviest stones.
    Since Python only has a Min Heap, we negate all weights.

    Time Complexity: O(n log n)
    Space Complexity: O(n)
    """
    # Python's heapq is a min-heap, so we negate values to simulate a max-heap
    max_heap = [-s for s in stones]
    heapq.heapify(max_heap)

    while len(max_heap) > 1:
        # Get the two heaviest stones
        first = -heapq.heappop(max_heap)
        second = -heapq.heappop(max_heap)

        if first != second:
            # Push the difference back if they are not equal
            heapq.heappush(max_heap, -(first - second))

    # If a stone remains, return its original (positive) weight, else 0
    return -max_heap[0] if max_heap else 0
```

### Explanation
1.  **Heap Initialization**: We use a max-heap (by negating values) to keep track of the stones. `heapify` takes $O(n)$ time.
2.  **Simulation**: We repeatedly extract the two largest elements using `heappop`.
3.  **Smashing**: If the stones have different weights, we calculate the remaining weight and push it back into the heap.
4.  **Termination**: The loop continues as long as there are at least two stones. Finally, we return the weight of the last stone if it exists.

### Complexity Analysis
- **Time Complexity**: $O(n \log n)$. Building the heap is $O(n)$. Each smash operation takes $O(\log n)$ to pop twice and $O(\log n)$ to push once. There are at most $n-1$ smashes.
- **Space Complexity**: $O(n)$ to store the heap.

---

## 2. Kth Largest Element in a Stream
Design a class to find the kth largest element in a stream. Note that it is the kth largest element in the sorted order, not the kth distinct element.
Implement `KthLargest` class:
- `KthLargest(int k, int[] nums)`: Initializes the object with the integer `k` and the stream of integers `nums`.
- `int add(int val)`: Appends the integer `val` to the stream and returns the element representing the kth largest element in the stream.

### Examples & Edge Cases
- **Example**: `k=3, nums=[4, 5, 8, 2]`. `add(3) -> 4`, `add(5) -> 5`, `add(10) -> 5`.
- **Edge Case: k > initial nums length**: The heap should grow until it reaches size `k`.
- **Edge Case: Duplicate values**: Should be handled correctly as per "sorted order" (not distinct).

### Optimal Python Solution
```python
import heapq

class KthLargest:
    """
    Maintain a min-heap of size k to track the k largest elements.
    The root of this min-heap will be the kth largest element.

    Time Complexity: O(n log k) for init, O(log k) for add
    Space Complexity: O(k)
    """
    def __init__(self, k: int, nums: list[int]):
        self.k = k
        self.heap = nums
        heapq.heapify(self.heap)

        # Keep only the k largest elements
        while len(self.heap) > k:
            heapq.heappop(self.heap)

    def add(self, val: int) -> int:
        # Add new value to the heap
        heapq.heappush(self.heap, val)

        # If heap exceeds size k, remove the smallest (which isn't in top-k)
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)

        # The root is the smallest of the top k elements, i.e., the kth largest
        return self.heap[0]
```

### Explanation
1.  **Min-Heap Strategy**: To find the $k$-th largest element, we maintain a min-heap of size $k$.
2.  **Why Min-Heap?**: In a min-heap of the $k$ largest elements, the root is the smallest among those $k$ elements, which effectively makes it the $k$-th largest overall.
3.  **Initialization**: We heapify the input and shrink it to size $k$.
4.  **Adding Elements**: When a new value comes, we push it. If the heap size exceeds $k$, we pop the minimum. This ensures we always keep the largest $k$ elements seen so far.

### Complexity Analysis
- **Time Complexity**:
    - `__init__`: $O(n \log k)$ or $O(n)$ if we heapify and then pop $n-k$ times.
    - `add`: $O(\log k)$ to maintain the heap of size $k$.
- **Space Complexity**: $O(k)$ to store the $k$ largest elements.

---

## 3. Sort an Array (Heap Sort)
Given an array of integers `nums`, sort the array in ascending order using the Heap Sort algorithm.

### Examples & Edge Cases
- **Example**: `nums = [5,2,3,1]` -> Output: `[1,2,3,5]`
- **Edge Case: Already sorted**: `[1,2,3]` -> `[1,2,3]`
- **Edge Case: Reverse sorted**: `[3,2,1]` -> `[1,2,3]`
- **Edge Case: Single element**: `[1]` -> `[1]`

### Optimal Python Solution
```python
def sortArray(nums: list[int]) -> list[int]:
    """
    In-place Heap Sort using a Max Heap.

    Time Complexity: O(n log n)
    Space Complexity: O(1) (excluding output)
    """
    def heapify(n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and nums[left] > nums[largest]:
            largest = left
        if right < n and nums[right] > nums[largest]:
            largest = right

        if largest != i:
            nums[i], nums[largest] = nums[largest], nums[i]
            heapify(n, largest)

    n = len(nums)

    # 1. Build Max Heap: O(n)
    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)

    # 2. Extract elements: O(n log n)
    for i in range(n - 1, 0, -1):
        # Move current root (max) to the end
        nums[i], nums[0] = nums[0], nums[i]
        # Restore heap property on the reduced heap
        heapify(i, 0)

    return nums
```

### Explanation
1.  **Build Max Heap**: We start from the last non-leaf node and move upwards, calling `heapify` to ensure the parent is larger than its children.
2.  **Sorting**: The largest element is always at `nums[0]`. We swap it with the last element of the current heap range, effectively "moving" the max to its sorted position.
3.  **Restore Heap**: We call `heapify` on the root with a reduced range size to find the next largest element.

### Complexity Analysis
- **Time Complexity**: $O(n \log n)$. Building the heap is $O(n)$. Each of the $n$ extractions takes $O(\log n)$.
- **Space Complexity**: $O(1)$ if done in-place, or $O(\log n)$ due to recursion stack. An iterative `heapify` would make it $O(1)$.

---

## 4. Kth Largest Element in an Array
Given an integer array `nums` and an integer `k`, return the kth largest element in the array.
Note that it is the kth largest element in the sorted order, not the kth distinct element.

### Examples & Edge Cases
- **Example**: `nums = [3,2,3,1,2,4,5,5,6], k = 4` -> Output: 4
- **Edge Case: k = 1**: Returns the maximum element.
- **Edge Case: k = n**: Returns the minimum element.

### Optimal Python Solution
```python
import heapq

def findKthLargest(nums: list[int], k: int) -> int:
    """
    Use a Min-Heap of size k.

    Time Complexity: O(n log k)
    Space Complexity: O(k)
    """
    # Initialize min-heap with first k elements
    min_heap = nums[:k]
    heapq.heapify(min_heap)

    # Process remaining elements
    for i in range(k, len(nums)):
        if nums[i] > min_heap[0]:
            # Replace the smallest in our top-k if current is larger
            heapq.heapreplace(min_heap, nums[i])

    return min_heap[0]
```

### Explanation
1.  **Selection Strategy**: Since we only need the $k$-th largest, keeping a heap of size $k$ is more space-efficient than sorting the whole array ($O(n \log n)$) or keeping a full heap ($O(n)$ space).
2.  **Algorithm**: We maintain the "top $k$" largest elements in a min-heap. The root (minimum) of these top $k$ is the $k$-th largest element.
3.  **Efficiency**: `heapreplace` is more efficient than `heappush` followed by `heappop`.

### Complexity Analysis
- **Time Complexity**: $O(n \log k)$. We iterate through the array once ($n$ elements), and each heap operation takes $\log k$.
- **Space Complexity**: $O(k)$ to store the heap.
