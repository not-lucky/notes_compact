# Container With Most Water

## Problem Statement

Given `n` non-negative integers `height` where each represents a point at coordinate `(i, height[i])`, find two lines that together with the x-axis form a container that contains the most water.

Return the maximum amount of water a container can store.

**Note:** You may not slant the container.

**Example:**
```
Input: height = [1, 8, 6, 2, 5, 4, 8, 3, 7]
Output: 49
Explanation: Lines at index 1 (height 8) and index 8 (height 7)
             Area = min(8, 7) × (8 - 1) = 7 × 7 = 49
```

## Building Intuition

### Why This Works

The area of a container is determined by two factors: width and height. Width is `right - left`, and height is `min(height[left], height[right])` because water can only rise to the shorter wall.

Starting with the widest possible container (pointers at both ends) gives us maximum width. From here, the only way to potentially increase area is to find taller walls. If we move the taller wall inward, we definitely lose width and cannot gain height (the shorter wall still limits us). So we must move the shorter wall, hoping to find a taller one.

This greedy choice is optimal: we never skip a pair that could be the answer. If the optimal pair is (i, j), we will consider it when our pointers reach those positions. We move away from a position only when it cannot possibly be part of a better solution.

### How to Discover This

When a problem involves pairs of elements where order matters (left < right), consider two pointers starting from both ends. This gives you O(n) time instead of O(n^2) brute force.

The key insight is the greedy rule: "Which pointer should I move?" Think about what each move loses (here, width) versus what it might gain (here, height). If moving one pointer can only make things worse, move the other one.

### Pattern Recognition

This is the **Two Pointers from Ends** pattern with a **Greedy Decision Rule**. It appears in:
- Container with most water (this problem)
- Trapping rain water (different calculation, similar traversal)
- Two Sum on sorted array
- Valid palindrome
- Any problem where you are optimizing over pairs with an ordering constraint

## When NOT to Use

- **When the greedy rule does not hold**: If moving either pointer could lead to improvement, you cannot use this approach without modification. You would need to explore both branches (leading to higher complexity).
- **When you need all pairs, not just the optimal one**: Two pointers finds one answer; it does not enumerate all pairs meeting some criterion.
- **When heights can be negative**: The min/max logic assumes non-negative heights. Negative heights would break the container analogy.
- **When the problem is "Trapping Rain Water"**: Despite visual similarity, trapping water measures water ON TOP of bars, not between two walls. It requires tracking running max from both sides, not just a simple min comparison.

## Approach

### Key Insight
Area is determined by: `min(height[left], height[right]) × (right - left)`

The width is maximized when we start with the widest possible container (leftmost and rightmost lines). Then we try to find lines that might give more height to compensate for reduced width.

### Two Pointer Strategy
1. Start with pointers at both ends (maximum width)
2. Calculate area
3. Move the pointer pointing to the shorter line inward
   - Why? The shorter line limits the height. Moving the taller line can only decrease or maintain the area (less width, same or less height)
4. Repeat until pointers meet

```
height = [1, 8, 6, 2, 5, 4, 8, 3, 7]
          L                       R

L=0, R=8: area = min(1,7) × 8 = 8   → move L (height 1 is limiting)
L=1, R=8: area = min(8,7) × 7 = 49  → move R (height 7 is limiting)
L=1, R=7: area = min(8,3) × 6 = 18  → move R
L=1, R=6: area = min(8,8) × 5 = 40  → move either (equal heights)
...continue until L >= R

Maximum: 49
```

## Implementation

```python
def max_area(height: list[int]) -> int:
    """
    Find maximum water container using two pointers.

    Time: O(n) - single pass
    Space: O(1) - only pointer variables
    """
    left = 0
    right = len(height) - 1
    max_water = 0

    while left < right:
        # Calculate area with current pointers
        width = right - left
        h = min(height[left], height[right])
        area = width * h
        max_water = max(max_water, area)

        # Move pointer with smaller height
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1

    return max_water


def max_area_optimized(height: list[int]) -> int:
    """
    Optimized version: Skip lines shorter than current min height.
    """
    left = 0
    right = len(height) - 1
    max_water = 0

    while left < right:
        h = min(height[left], height[right])
        max_water = max(max_water, h * (right - left))

        # Skip all lines shorter than current height
        while left < right and height[left] <= h:
            left += 1
        while left < right and height[right] <= h:
            right -= 1

    return max_water
```

## Complexity Analysis

| Aspect | Complexity | Explanation |
|--------|------------|-------------|
| Time | O(n) | Each pointer moves at most n times |
| Space | O(1) | Only two pointer variables |

## Why Two Pointers Work (Proof)

The greedy choice is optimal because:

1. We start with maximum width
2. When we move the shorter line inward, we're the only way to potentially increase area
3. Moving the taller line would definitely reduce area (less width, height stays same or decreases)
4. We never skip a potentially optimal pair

**Formal argument:** For any optimal pair (i, j), the algorithm will consider both height[i] and height[j] before moving past either of them. When considering this pair:
- If it's the current pair, we calculate its area
- If not, we haven't moved past either endpoint, so we'll reach it eventually

## Edge Cases

1. **Two elements**: `[1, 1]` → Area = 1
2. **Decreasing heights**: `[5, 4, 3, 2, 1]` → Check all pairs
3. **Increasing heights**: `[1, 2, 3, 4, 5]` → Similar handling
4. **All same heights**: `[5, 5, 5, 5]` → Width matters most
5. **One tall line**: `[1, 1, 100, 1, 1]` → Bounded by shorter lines
6. **Zeros**: `[0, 2, 0]` → Area can be 0

## Common Mistakes

1. **Moving wrong pointer**: Always move the shorter one
2. **Off-by-one in width**: Width is `right - left`, not `right - left + 1`
3. **Using height sum instead of min**: Container height is min of two lines
4. **Brute force in interview**: O(n²) is too slow for large inputs

## Visual Explanation

```
height = [1, 8, 6, 2, 5, 4, 8, 3, 7]

8 │    │           │
7 │    │           │     │
6 │    │  │        │     │
5 │    │  │  │     │     │
4 │    │  │  │  │  │     │
3 │    │  │  │  │  │  │  │
2 │    │  │  │  │  │  │  │
1 │  │ │  │  │  │  │  │  │
  └───────────────────────────
     0  1  2  3  4  5  6  7  8

Container between index 1 and 8:
- Height = min(8, 7) = 7
- Width = 8 - 1 = 7
- Area = 49
```

## Variations

### Trapping Rain Water (Different Problem!)
This calculates water trapped ON TOP of bars, not between two lines.

```python
def trap(height: list[int]) -> int:
    """
    Water trapped above bars, not between two lines.
    Uses two pointers but different logic.
    """
    if not height:
        return 0

    left, right = 0, len(height) - 1
    left_max, right_max = height[left], height[right]
    water = 0

    while left < right:
        if left_max < right_max:
            left += 1
            left_max = max(left_max, height[left])
            water += left_max - height[left]
        else:
            right -= 1
            right_max = max(right_max, height[right])
            water += right_max - height[right]

    return water
```

## Related Problems

- **Trapping Rain Water** - Water trapped on bars (different approach)
- **Largest Rectangle in Histogram** - Monotonic stack
- **Maximal Rectangle** - 2D version with histogram
- **3Sum** - Two pointer technique
