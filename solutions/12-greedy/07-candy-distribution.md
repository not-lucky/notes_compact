# Solutions: Candy Distribution

## 1. Candy

**Problem Statement**:
There are `n` children standing in a line. Each child is assigned a rating value given in the integer array `ratings`. You are giving candies to these children subjected to the following requirements:

1. Each child must have at least one candy.
2. Children with a higher rating get more candies than their neighbors.

Return the minimum number of candies you need to have to distribute the candies to the children.

**Examples & Edge Cases**:

- **Example 1**:
  - Input: `ratings = [1,0,2]`
  - Output: `5`
  - Explanation: You can allocate to the first, second and third child with 2, 1, 2 candies respectively.
- **Example 2**:
  - Input: `ratings = [1,2,2]`
  - Output: `4`
  - Explanation: You can allocate to the first, second and third child with 1, 2, 1 candies respectively. The third child gets 1 candy because it satisfies the above two conditions (it doesn't have a higher rating than its left neighbor, so it doesn't _need_ more).
- **Edge Cases**:
  - All same ratings: Everyone gets 1.
  - Strictly increasing: [1, 2, 3, ...].
  - Strictly decreasing: [..., 3, 2, 1].

**Optimal Python Solution (Two-Pass Greedy)**:

```python
def candy(ratings: list[int]) -> int:
    """
    Two-pass greedy solution to handle left and right neighbor constraints.
    """
    n = len(ratings)
    if n == 0:
        return 0

    # Requirement 1: Each child must have at least one candy.
    candies = [1] * n

    # Pass 1 (Left to Right): Handle the left-neighbor constraint.
    # If a child has a higher rating than their left neighbor,
    # they must have more candy.
    for i in range(1, n):
        if ratings[i] > ratings[i-1]:
            candies[i] = candies[i-1] + 1

    # Pass 2 (Right to Left): Handle the right-neighbor constraint.
    # If a child has a higher rating than their right neighbor,
    # they must have more candy. We use max() to ensure we don't
    # violate the left-neighbor constraint satisfied in Pass 1.
    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i+1]:
            # They need more than the right neighbor (candies[i+1] + 1)
            # but they also need to keep their current count if it was
            # already higher due to their left neighbor.
            candies[i] = max(candies[i], candies[i+1] + 1)

    return sum(candies)
```

**Explanation**:

1.  **Why Two Passes?**: A single pass (left-to-right) can only ensure that a child has more candy than their left neighbor. It has no information about the right neighbor.
2.  **Left Pass**: We ensure `if ratings[i] > ratings[i-1] then candies[i] > candies[i-1]`.
3.  **Right Pass**: We ensure `if ratings[i] > ratings[i+1] then candies[i] > candies[i+1]`. By starting from the right and using `max()`, we update the counts to satisfy both neighbors while keeping the total candy count at a minimum.
4.  **Local Optimality**: At each step, we provide the _minimum_ possible candy to satisfy the immediate constraint, which leads to a globally minimal sum.

**Complexity Analysis**:

- **Time Complexity**: `O(N)`, where `N` is the number of children. We do two linear scans.
- **Space Complexity**: `O(N)` to store the candy counts.

---

## 2. Trapping Rain Water

**Problem Statement**:
Given `n` non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.

**Examples & Edge Cases**:

- **Example 1**:
  - Input: `height = [0,1,0,2,1,0,1,3,2,1,2,1]`
  - Output: `6`
- **Edge Cases**:
  - Array length < 3: Cannot trap any water.
  - Monotonically increasing or decreasing: No "valleys", so 0 water.

**Optimal Python Solution (Two-Pass Greedy / DP)**:

```python
def trap(height: list[int]) -> int:
    """
    Calculate trapped water by finding the 'ceiling' at each position.
    The ceiling is determined by the max height to the left and right.
    """
    if not height:
        return 0

    n = len(height)
    left_max = [0] * n
    right_max = [0] * n

    # Pass 1: Find the maximum height to the left of each index
    left_max[0] = height[0]
    for i in range(1, n):
        left_max[i] = max(left_max[i-1], height[i])

    # Pass 2: Find the maximum height to the right of each index
    right_max[n-1] = height[n-1]
    for i in range(n-2, -1, -1):
        right_max[i] = max(right_max[i+1], height[i])

    # The water level at index i is min(left_max[i], right_max[i])
    trapped_water = 0
    for i in range(n):
        # Water = height of ceiling - height of ground
        trapped_water += min(left_max[i], right_max[i]) - height[i]

    return trapped_water
```

**Explanation**:

1.  **Intuition**: For any spot `i`, the amount of water it can hold depends on the "walls" to its left and right. Specifically, it's the minimum of the highest wall on the left and the highest wall on the right.
2.  **Two-Pass Pattern**: We pre-calculate these left and right peaks.
    - `left_max[i]` stores the max height from `0` to `i`.
    - `right_max[i]` stores the max height from `i` to `n-1`.
3.  **Calculation**: The "ceiling" at `i` is `min(left_max[i], right_max[i])`. The water trapped is `ceiling - height[i]`.

**Complexity Analysis**:

- **Time Complexity**: `O(N)`.
- **Space Complexity**: `O(N)` for the two auxiliary arrays. (Can be optimized to `O(1)` using two pointers).

---

## 3. Product of Array Except Self

**Problem Statement**:
Given an integer array `nums`, return an array `answer` such that `answer[i]` is equal to the product of all the elements of `nums` except `nums[i]`. You must solve it in `O(n)` and without using the division operation.

**Examples & Edge Cases**:

- **Example 1**:
  - Input: `nums = [1,2,3,4]`
  - Output: `[24,12,8,6]`
- **Edge Cases**:
  - Array contains zeros.

**Optimal Python Solution (Prefix and Suffix Products)**:

```python
def productExceptSelf(nums: list[int]) -> list[int]:
    """
    Use prefix and suffix products to calculate the result without division.
    """
    n = len(nums)
    res = [1] * n

    # Pass 1: Calculate prefix products
    # res[i] will contain the product of all elements to the left of i
    prefix = 1
    for i in range(n):
        res[i] = prefix
        prefix *= nums[i]

    # Pass 2: Multiply by suffix products
    # Multiply current res[i] by the product of all elements to the right
    suffix = 1
    for i in range(n - 1, -1, -1):
        res[i] *= suffix
        suffix *= nums[i]

    return res
```

**Explanation**:

1.  **Decomposition**: The product of all elements except `nums[i]` is: `(product of elements before i) * (product of elements after i)`.
2.  **Forward Pass**: We calculate the "prefix product" and store it in the result array.
3.  **Backward Pass**: We maintain a running "suffix product" and multiply it into our existing prefix products.
4.  **No Division**: This elegantly handles the no-division constraint and the zero-element edge cases.

**Complexity Analysis**:

- **Time Complexity**: `O(N)`.
- **Space Complexity**: `O(1)` if we don't count the output array.

---

## 4. Container With Most Water

**Problem Statement**:
You are given an integer array `height` of length `n`. There are `n` vertical lines drawn such that the two endpoints of the `i-th` line are `(i, 0)` and `(i, height[i])`. Find two lines that together with the x-axis form a container, such that the container contains the most water. Return the maximum amount of water a container can store.

**Optimal Python Solution (Two-Pointer Greedy)**:

```python
def maxArea(height: list[int]) -> int:
    """
    Two-pointer greedy: Move the pointer that points to the shorter line.
    """
    left = 0
    right = len(height) - 1
    max_val = 0

    while left < right:
        # Calculate area: (width) * min_height
        current_area = (right - left) * min(height[left], height[right])
        max_val = max(max_val, current_area)

        # Greedy Choice: move the shorter wall, as it limits the height
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1

    return max_val
```

**Explanation**:

1.  **Intuition**: The area is limited by the shorter of the two lines. To find a larger area, we must replace the shorter line with a potentially taller one.
2.  **Greedy Choice**: We start with the widest possible container (first and last lines). Then, we greedily move the pointer that points to the shorter line, hoping to find a taller line that compensates for the decreased width.
3.  **Efficiency**: This allows us to find the global maximum in `O(N)` without checking all `O(N^2)` pairs.

**Complexity Analysis**:

- **Time Complexity**: `O(N)`.
- **Space Complexity**: `O(1)`.

---

## 5. Increasing Triplet Subsequence

**Problem Statement**:
Given an integer array `nums`, return `true` if there exists a triple of indices `(i, j, k)` such that `i < j < k` and `nums[i] < nums[j] < nums[k]`. If no such indices exist, return `false`.

**Optimal Python Solution (Greedy Tracking)**:

```python
def increasingTriplet(nums: list[int]) -> bool:
    """
    Greedy tracking of the two smallest elements seen so far.
    """
    first = float('inf')
    second = float('inf')

    for n in nums:
        if n <= first:
            # Found a new smallest element
            first = n
        elif n <= second:
            # Found an element larger than first but smaller than second
            second = n
        else:
            # Found an element larger than both first and second!
            return True

    return False
```

**Explanation**:

1.  **Greedy Logic**: We want to keep `first` and `second` as small as possible to maximize the chance of finding a third element larger than both.
2.  **Update Rule**:
    - If current `n` is smaller than `first`, update `first`.
    - Else if `n` is smaller than `second`, update `second`.
    - Else, `n` is larger than both, meaning we've found our triplet.
3.  **Why it works**: Even if `first` is updated _after_ `second` was set (meaning the actual `first` that made `second` valid is further left), the fact that we found something larger than `second` still guarantees a triplet exists.

**Complexity Analysis**:

- **Time Complexity**: `O(N)`.
- **Space Complexity**: `O(1)`.
