# Greedy Basics

> **Prerequisites:** [Dynamic Programming Basics](../09-dynamic-programming/01-dp-fundamentals.md)

## Interview Context

Greedy basics test:
1. **Algorithm design**: Can you recognize when greedy applies?
2. **Proof skills**: Can you argue why greedy gives optimal solution?
3. **Counter-examples**: Can you identify when greedy fails?
4. **Trade-off awareness**: Understanding greedy vs DP trade-offs

---

## What is a Greedy Algorithm?

A greedy algorithm makes the **locally optimal choice** at each step, hoping to find the **global optimum**.

```
General Greedy Structure:
1. Sort/order choices by some criteria
2. Iterate through choices
3. At each step, take the best available option
4. Never reconsider previous choices
```

### Key Characteristics

- **Irrevocable decisions**: Once a choice is made, it's never changed
- **Local optimization**: Each step picks what looks best now
- **Efficiency**: Usually O(n) or O(n log n) time
- **Simplicity**: Easier to implement than DP

---

## When Does Greedy Work?

### Two Required Properties

#### 1. Greedy Choice Property

Making the locally optimal choice is part of some globally optimal solution.

```python
# Example: Activity Selection
# Greedy choice: Pick activity with earliest end time
# Why it works: Leaves maximum room for remaining activities

def activity_selection(activities):
    """
    Pick maximum non-overlapping activities.
    Greedy: always pick earliest-ending available activity.
    """
    # Sort by end time
    activities.sort(key=lambda x: x[1])

    result = [activities[0]]  # Pick first (earliest end)
    last_end = activities[0][1]

    for start, end in activities[1:]:
        if start >= last_end:  # Non-overlapping
            result.append((start, end))
            last_end = end

    return result
```

#### 2. Optimal Substructure

An optimal solution contains optimal solutions to subproblems.

```
After making the greedy choice:
- The remaining problem is a smaller instance
- The optimal solution to remaining problem + greedy choice
  = optimal solution to original problem
```

---

## Proof Techniques

### 1. Greedy Stays Ahead

Show that at every step, greedy is at least as good as any other approach.

```
Proof for Activity Selection:
1. Let G = greedy solution, O = any optimal solution
2. Let g₁, g₂, ... be activities in G (sorted by end time)
3. Let o₁, o₂, ... be activities in O (sorted by end time)

Claim: end(gᵢ) ≤ end(oᵢ) for all i

Proof by induction:
- Base: g₁ ends earliest by construction, so end(g₁) ≤ end(o₁) ✓
- Step: If end(gᵢ) ≤ end(oᵢ), then gᵢ₊₁ can be any activity
        after end(gᵢ). Since greedy picks earliest-ending,
        end(gᵢ₊₁) ≤ end(oᵢ₊₁) ✓

Since greedy never falls behind, |G| ≥ |O|.
```

### 2. Exchange Argument

Show any optimal solution can be transformed to greedy solution without worsening it.

```
Proof for Huffman Coding:
1. Let T be any optimal tree
2. Let x, y be two lowest-frequency symbols
3. If x, y aren't siblings at max depth in T:
   - Swap them to be siblings at max depth
   - This doesn't increase cost (they have lowest frequencies)
4. This matches greedy's first choice
5. Recursively apply to remaining tree
6. Result: optimal tree = greedy tree
```

### 3. Contradiction

Assume greedy isn't optimal, derive a contradiction.

```
Proof for Fractional Knapsack:
1. Assume greedy (by value/weight ratio) isn't optimal
2. Some optimal solution O doesn't take most of highest-ratio item
3. Swap some of O's items for more of highest-ratio item
4. This increases total value (higher ratio = better value per weight)
5. Contradiction: O wasn't optimal after all
```

---

## Classic Greedy Problems

### Example 1: Fractional Knapsack

```python
def fractional_knapsack(items: list[tuple[int, int]], capacity: int) -> float:
    """
    Maximize value with fractional items allowed.

    Args:
        items: List of (value, weight) tuples
        capacity: Maximum weight capacity

    Returns:
        Maximum value achievable

    Time: O(n log n)
    Space: O(1)
    """
    # Sort by value/weight ratio (descending)
    items = sorted(items, key=lambda x: x[0] / x[1], reverse=True)

    total_value = 0.0
    remaining = capacity

    for value, weight in items:
        if weight <= remaining:
            # Take the whole item
            total_value += value
            remaining -= weight
        else:
            # Take fraction of item
            fraction = remaining / weight
            total_value += value * fraction
            break  # Knapsack is full

    return total_value
```

### Why Greedy Works Here (But Fails for 0/1 Knapsack)

```
Fractional Knapsack: Greedy Works ✓
- Can take fractions, so highest ratio always best
- No "all or nothing" constraint

0/1 Knapsack: Greedy Fails ✗
- items = [(60, 10), (100, 20), (120, 30)], capacity = 50
- Greedy (by ratio): Take 60/10=6, 100/20=5 → value=160
- Optimal: Take 100/20 + 120/30 → value=220
```

### Example 2: Assign Cookies

```python
def find_content_children(greed: list[int], cookies: list[int]) -> int:
    """
    Assign cookies to children to maximize satisfied children.
    Child i is satisfied if cookie size >= greed[i].

    Time: O(n log n + m log m)
    Space: O(1)
    """
    greed.sort()
    cookies.sort()

    child = 0
    cookie = 0

    while child < len(greed) and cookie < len(cookies):
        if cookies[cookie] >= greed[child]:
            # This cookie satisfies this child
            child += 1
        # Try next cookie regardless
        cookie += 1

    return child  # Number of satisfied children
```

### Example 3: Lemonade Change

```python
def lemonade_change(bills: list[int]) -> bool:
    """
    Give correct change for $5 lemonade.
    Bills can be $5, $10, or $20.

    Greedy: Always use $10 before $5s for $15 change.

    Time: O(n)
    Space: O(1)
    """
    five = ten = 0

    for bill in bills:
        if bill == 5:
            five += 1
        elif bill == 10:
            if five == 0:
                return False
            five -= 1
            ten += 1
        else:  # bill == 20
            # Prefer giving $10 + $5 over $5 + $5 + $5
            if ten > 0 and five > 0:
                ten -= 1
                five -= 1
            elif five >= 3:
                five -= 3
            else:
                return False

    return True
```

---

## When Greedy Fails

### Example: Coin Change

```python
def coin_change_greedy(coins: list[int], amount: int) -> int:
    """
    WRONG for arbitrary coin denominations!
    """
    coins.sort(reverse=True)  # Largest first
    count = 0

    for coin in coins:
        while amount >= coin:
            amount -= coin
            count += 1

    return count if amount == 0 else -1


# Test case showing failure:
# coins = [1, 3, 4], amount = 6
# Greedy: 4 + 1 + 1 = 3 coins
# Optimal: 3 + 3 = 2 coins
```

### Why Greedy Fails

```
Greedy choice (largest coin) doesn't lead to optimal solution.
The locally best choice (take 4) prevents the globally best solution (two 3s).

Counter-intuitive: taking a smaller coin now leads to better overall result.

This is why coin change (general) needs DP:
- We must consider ALL ways to make each sub-amount
- Can't greedily commit to any single coin choice
```

---

## Greedy vs DP Decision Tree

```
Can the problem be solved greedily?
    │
    ├── Can you prove greedy choice property?
    │   │
    │   ├── Yes → Try greedy, verify with examples
    │   │
    │   └── No / Unsure → Use DP
    │
    ├── Do later choices depend on earlier ones?
    │   │
    │   ├── No (independent) → Greedy may work
    │   │
    │   └── Yes (overlapping subproblems) → Use DP
    │
    └── Can you find a counter-example?
        │
        ├── Yes → Greedy fails, use DP
        │
        └── No → Greedy likely works (but verify)
```

---

## Common Greedy Patterns

| Pattern | Strategy | Examples |
|---------|----------|----------|
| **Sorting First** | Sort by key attribute, then iterate | Activity selection, meeting rooms |
| **Two Pointers** | Greedy matching from both ends | Assign cookies, boats to save people |
| **Track Reachability** | Maintain what's achievable | Jump game, gas station |
| **Two Pass** | Forward pass + backward pass | Candy distribution |
| **Heap-based** | Always process min/max first | Task scheduler, merge k lists |

---

## Complexity Analysis

| Operation | Time | Space | Notes |
|-----------|------|-------|-------|
| Sort-based greedy | O(n log n) | O(1) | Sorting dominates |
| Single pass | O(n) | O(1) | Linear scan |
| Two pass | O(n) | O(n) | Forward + backward |
| Heap-based | O(n log n) | O(n) | Heap operations |

---

## Edge Cases

- [ ] Empty input → usually return 0 or base case
- [ ] Single element → often the answer itself
- [ ] All same values → ties need handling
- [ ] Already sorted input → algorithm should still work
- [ ] Counter-examples → test greedy assumption

---

## Practice Problems

| # | Problem | Difficulty | Key Insight |
|---|---------|------------|-------------|
| 1 | Assign Cookies | Easy | Sort both, greedy matching |
| 2 | Lemonade Change | Easy | Greedy change giving |
| 3 | Best Time to Buy and Sell Stock II | Medium | Collect all profits |
| 4 | Boats to Save People | Medium | Two-pointer greedy |
| 5 | Minimum Number of Arrows to Burst Balloons | Medium | Interval greedy |

---

## Interview Tips

1. **State the greedy strategy clearly**: "I'll sort by X and greedily pick Y"
2. **Justify why it works**: Prove or argue greedy choice property
3. **Consider counter-examples**: Think about when greedy might fail
4. **Compare to DP**: Explain why DP isn't needed (or is)
5. **Verify with examples**: Trace through the algorithm manually

---

## Key Takeaways

1. Greedy makes locally optimal choices hoping for global optimum
2. Works when problem has greedy choice property + optimal substructure
3. Three proof techniques: stays ahead, exchange, contradiction
4. Faster than DP but doesn't always work
5. Counter-examples are the best way to disprove greedy applicability

---

## Next: [02-interval-scheduling.md](./02-interval-scheduling.md)

Learn the classic interval scheduling pattern: activity selection and maximum meetings.
