# Greedy Basics

> **Note:** Greedy algorithms are often contrasted with dynamic programming. While DP is covered in [Chapter 9](../09-dynamic-programming/README.md), this chapter is self-contained and can be read independently.

## Interview Context

Greedy basics test:

1. **Algorithm design**: Can you recognize when greedy applies?
2. **Proof skills**: Can you argue why greedy gives an optimal solution?
3. **Counter-examples**: Can you identify when greedy fails?
4. **Trade-off awareness**: Understanding greedy vs DP trade-offs

---

## Building Intuition

**Why Does Greedy Sometimes Work?**

Imagine you're at a buffet with limited plate space. The greedy strategy is: "Take the best thing you see right now." This works if:

1. What's "best" doesn't change based on what you've already taken
2. Taking the best thing now never blocks you from an even better overall outcome

The key insight is that some problems have this "no regrets" property: making the locally best choice is always safe because it's part of _some_ optimal solution.

**The "Irrevocable Decision" Model**

Think of greedy as a one-way door. Once you walk through, you can't go back. DP, by contrast, explores all paths and picks the globally best one.

```text
Greedy:    Choice A --> Choice B --> Choice C --> Done
           (Each choice is final, no backtracking)

DP:        Consider A  -->  Consider B  -->  Consider C
                |                |                |
           All options     All options      All options
                |                |                |
           Pick best       Pick best        Pick best
           (Remembers all subproblem results, picks globally best)
```

**When Does "Locally Best = Globally Best"?**

The greedy approach works when:

1. **No blocking**: Choosing item X doesn't prevent a better combination involving Y
2. **Safe commitment**: Each greedy choice is part of _some_ optimal solution (greedy choice property)
3. **Reducibility**: After the greedy choice, the remaining problem is a smaller instance of the same type (optimal substructure)

Counter-example -- why greedy fails for 0/1 knapsack:

```text
Items: [(value=60, weight=10), (value=100, weight=20), (value=120, weight=30)]
Capacity: 50

Greedy by value/weight ratio:
- Item 1: ratio = 6.0  <-- pick first  (10kg used, 40kg left)
- Item 2: ratio = 5.0  <-- pick second (30kg used, 20kg left)
- Item 3: ratio = 4.0  <-- can't fit   (needs 30kg, only 20kg left)
Result: 60 + 100 = 160

Optimal:
- Skip item 1
- Take items 2 + 3: 100 + 120 = 220

The problem: taking item 1 BLOCKED the better combination.
This "blocking" is why greedy fails -- you can't take fractions to recover.
```

---

## What is a Greedy Algorithm?

A greedy algorithm makes the **locally optimal choice** at each step, aiming to reach the **global optimum**.

```text
General Greedy Structure:
1. Identify the greedy criterion (what makes a choice "best")
2. Sort/order choices by that criterion (if needed)
3. Iterate through choices
4. At each step, take the best available option
5. Never reconsider previous choices

Note: Not all greedy algorithms require sorting. Some work with a single
linear scan where the greedy choice is apparent at each step (e.g.,
tracking maximum reach so far in Jump Game).
```

### Key Characteristics

- **Irrevocable decisions**: Once a choice is made, it's never changed
- **Local optimization**: Each step picks what looks best now
- **Efficiency**: Usually $O(n)$ or $O(n \log n)$ time
- **Simplicity**: Easier to implement than DP

---

## When Does Greedy Work?

### Two Required Properties

#### 1. Greedy Choice Property

There **exists** an optimal solution that includes the locally optimal choice. In other words, committing to the greedy choice never disqualifies us from reaching an optimum.

```python
# Example: Activity Selection
# Greedy choice: pick activity with earliest end time
# Why it works: leaves maximum room for remaining activities

def activity_selection(activities: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """
    Select maximum number of non-overlapping activities.
    Greedy strategy: always pick the activity with earliest end time.

    Time:  O(n log n) -- sorting dominates
    Space: O(n) -- for the sorted copy and result list
    """
    if not activities:
        return []

    # Sort by end time
    sorted_activities = sorted(activities, key=lambda x: x[1])

    result = [sorted_activities[0]]
    last_end = sorted_activities[0][1]

    for start, end in sorted_activities[1:]:
        if start >= last_end:
            result.append((start, end))
            last_end = end

    return result
```

**Visual trace:**

```text
Activities: [(1,4), (3,5), (0,6), (5,7), (3,9), (5,9), (6,10), (8,11), (8,12), (2,14), (12,16)]

Sorted by end time:
  (1,4)  (3,5)  (0,6)  (5,7)  (3,9)  (5,9)  (6,10) (8,11) (8,12) (2,14) (12,16)

Timeline:
0    2    4    6    8    10   12   14   16
|----|----|----|----|----|----|----|----|
[=1,4=]                                   PICK (first activity)
   [=3,5==]                                skip (3 < 4, overlaps)
[===0,6====]                               skip (0 < 4, overlaps)
          [5,7]                            PICK (5 >= 4)
     [===3,9========]                      skip (3 < 7, overlaps)
          [===5,9====]                     skip (5 < 7, overlaps)
            [==6,10===]                    skip (6 < 7, overlaps)
                [=8,11==]                  PICK (8 >= 7)
                [==8,12===]                skip (8 < 11, overlaps)
  [==========2,14===========]              skip (2 < 11, overlaps)
                       [12,16]             PICK (12 >= 11)

Result: [(1,4), (5,7), (8,11), (12,16)] -- 4 activities
```

#### 2. Optimal Substructure

An optimal solution to the whole problem contains optimal solutions to its subproblems.

```text
After making the greedy choice:
- The remaining problem is a smaller instance of the same type
- Optimal solution = greedy choice + optimal solution to remaining subproblem
- This is what lets us reduce the problem by one choice at each step

Example (Activity Selection):
  Original problem: maximize activities from {A, B, C, D, E}
  Greedy picks A (earliest end time)
  Remaining problem: maximize activities from {C, D, E} (those not conflicting with A)
  This remaining problem has the SAME structure -- just fewer activities.
  Optimal for whole = {A} + optimal for remaining.
```

> **Note:** DP also requires optimal substructure. The difference is that greedy
> additionally needs the greedy choice property, which lets it commit to one
> subproblem instead of exploring all of them.

---

## When Greedy Fails

### Example: Coin Change

```python
# WRONG for arbitrary coin denominations!
def coin_change_greedy(coins: list[int], amount: int) -> int:
    """
    Greedy coin change -- INCORRECT for arbitrary denominations.
    Only works for canonical coin systems (like US coins).

    Time:  O(n log n) -- sorting dominates (n = number of denominations)
    Space: O(n) -- for the sorted copy
    """
    # Sort descending so we try largest coins first
    sorted_coins = sorted(coins, reverse=True)
    remaining = amount
    count = 0

    for coin in sorted_coins:
        if remaining == 0:
            break
        if coin <= remaining:
            count += remaining // coin
            remaining %= coin

    return count if remaining == 0 else -1

# Test case showing failure:
# coins = [1, 3, 4], amount = 6
# Greedy: 4 + 1 + 1 = 3 coins
# Optimal: 3 + 3 = 2 coins
```

### Why It Fails

```text
Greedy choice (largest coin) doesn't lead to optimal solution.
The locally best choice (take 4) prevents the globally best solution (two 3s).

Step-by-step trace for coins=[1,3,4], amount=6:

Greedy approach:
  1. Take coin 4 (largest that fits): remaining = 6 - 4 = 2
  2. Take coin 1 (largest that fits): remaining = 2 - 1 = 1
  3. Take coin 1 (largest that fits): remaining = 1 - 1 = 0
  Total: 3 coins (4 + 1 + 1)

Optimal solution:
  1. Take coin 3: remaining = 6 - 3 = 3
  2. Take coin 3: remaining = 3 - 3 = 0
  Total: 2 coins (3 + 3)

This is why coin change (general) needs DP:
- We must consider ALL ways to make each sub-amount
- Can't greedily commit to any single coin choice
```

(DP is needed here because the optimal way to make `6` depends on knowing
the optimal way to make `6-4=2`, `6-3=3`, and `6-1=5`.)

> **Interview note:** Greedy _does_ work for **canonical coin systems** like US
> coins `[1, 5, 10, 25]`. A coin system is canonical when the greedy algorithm
> (largest denomination first) always produces the minimum number of coins.
> There's no simple rule to determine this -- for arbitrary denominations, always
> use DP.
>
> **Practical tip:** If asked about coin change in an interview, clarify whether
> the coin system is canonical. If unsure, implement DP and mention that greedy
> only works for special coin systems.

### When NOT to Use Greedy

**1. Lack of Greedy Choice Property**

The most common reason greedy fails: making the best local choice blocks the global optimum, as shown in the coin change example above.

**2. When You Can't Define a Clear "Greedy Ordering"**

If you can't sort or prioritize elements by a single criterion that guarantees optimality, greedy likely fails.

**3. When All-or-Nothing Constraints Exist**

0/1 Knapsack fails because you can't take partial items. Fractional knapsack works because you CAN take fractions, removing the "blocking" problem.

**4. When Path Dependencies Exist**

If reaching node A via path X gives different options than reaching A via path Y, greedy may miss optimal paths.

**Red flags (greedy probably won't work):**

| Red Flag | Why Greedy Fails | Alternative |
| --- | --- | --- |
| "Choose exactly k items" | Subset selection often needs DP | DP with state tracking count |
| "Minimize/maximize subject to multiple constraints" | Multiple constraints create complex trade-offs | DP, ILP, or multi-objective optimization |
| "Count all ways" | Greedy makes one choice, can't enumerate | DP with counting |
| "Find all valid configurations" | Greedy commits to one path | Backtracking / DFS |
| "Minimum edits/operations" | Local optimum may require multiple changes | DP (e.g., edit distance) |

---

## Proof Techniques

### 1. Greedy Stays Ahead

Show that at every step, greedy is at least as good as any other approach.

```text
Proof for Activity Selection:
1. Let G = greedy solution, O = any optimal solution
2. Let g1, g2, ... be activities in G (sorted by end time)
3. Let o1, o2, ... be activities in O (sorted by end time)

Claim: end(gi) <= end(oi) for all i

Proof by induction:
- Base: g1 ends earliest by construction, so end(g1) <= end(o1)
- Step: Assume end(gi) <= end(oi). Then every activity available
        after oi is also available after gi (it ends no later).
        Greedy picks the earliest-ending from this (at-least-as-large) set,
        so end(g(i+1)) <= end(o(i+1))

Since greedy never falls behind, |G| >= |O|.
```

### 2. Exchange Argument

Show any optimal solution can be transformed into the greedy solution without worsening it.

```text
Proof for Huffman Coding:
1. Let T be any optimal tree
2. Let x, y be two lowest-frequency symbols
3. If x, y aren't siblings at max depth in T:
   - Swap them to be siblings at max depth
   - This doesn't increase cost (they have lowest frequencies,
     so placing them at max depth is at least as good)
4. This matches greedy's first choice
5. Recursively apply to remaining tree
6. Result: optimal tree = greedy tree
```

### 3. Contradiction

Assume greedy isn't optimal, derive a contradiction.

```text
Proof for Fractional Knapsack:
1. Assume greedy (by value/weight ratio) isn't optimal
2. Some optimal solution O takes less of the highest-ratio item
3. Replace some lower-ratio weight in O with more of the highest-ratio item
4. This strictly increases total value (higher ratio = better value per weight)
5. Contradiction: O wasn't optimal after all
```

---

## Classic Greedy Problems

### Example 1: Fractional Knapsack

```python
def fractional_knapsack(items: list[tuple[float, float]], capacity: float) -> float:
    """
    Maximize value with fractional items allowed.

    Greedy strategy: Take items in order of value/weight ratio (highest first).
    When we can't fit a whole item, take the fraction that fills remaining capacity.

    Time:  O(n log n) -- sorting dominates
    Space: O(n) -- for the filtered/sorted copy
    """
    valid_items = [(v, w) for v, w in items if w > 0]
    # Sort by value-to-weight ratio in descending order
    valid_items = sorted(valid_items, key=lambda x: x[0] / x[1], reverse=True)

    total_value = 0.0
    remaining = capacity

    for value, weight in valid_items:
        if weight <= remaining:
            total_value += value
            remaining -= weight
        else:
            total_value += value * (remaining / weight)
            break  # Knapsack is full

    return total_value
```

**Visual trace:**

```text
items = [(60, 10), (100, 20), (120, 30)], capacity = 50

Ratios: 60/10=6.0, 100/20=5.0, 120/30=4.0
Sorted by ratio (desc): [(60,10), (100,20), (120,30)]

Take (60, 10):  full item, +60   (remaining: 40)
Take (100, 20): full item, +100  (remaining: 20)
Take (120, 30): only 20/30 fits, +120*(20/30) = +80

Total: 60 + 100 + 80 = 240
```

**Why greedy works here but fails for 0/1 knapsack:**

- **Fractional**: Can take fractions, so the highest ratio is always the best marginal choice. No "all or nothing" constraint means no blocking.
- **0/1**: Must take whole items, so a high-ratio item can block a better combination. See the counter-example in "Building Intuition" above.

### Example 2: Assign Cookies (LC 455)

**Why greedy works:** Sort both arrays. Assign the smallest cookie that satisfies the least greedy child. Using a bigger cookie than necessary would waste capacity that could satisfy a greedier child later.

```python
def find_content_children(greed: list[int], cookies: list[int]) -> int:
    """
    Assign cookies to children to maximize satisfied children.
    Child i is satisfied if cookie size >= greed[i].

    Greedy strategy: Assign the smallest cookie that satisfies the least greedy child.
    This preserves larger cookies for children with higher greed factors.

    Time:  O(n log n + m log m) -- sorting both arrays
    Space: O(n + m) -- for the sorted copies (using sorted() to avoid side effects)
    """
    sorted_greed = sorted(greed)
    sorted_cookies = sorted(cookies)

    child = 0

    for cookie in sorted_cookies:
        if child == len(sorted_greed):
            break  # All children satisfied
        if cookie >= sorted_greed[child]:
            child += 1

    return child
```

**Visual trace:**

```text
greed   = [1, 2, 3]    (children want at least this size)
cookies = [1, 1, 3]    (available cookie sizes)

After sorting: sorted_greed = [1, 2, 3], sorted_cookies = [1, 1, 3]

cookie=1: sorted_greed[0]=1, 1 >= 1? Yes -> child=1
cookie=1: sorted_greed[1]=2, 1 >= 2? No  -> skip
cookie=3: sorted_greed[1]=2, 3 >= 2? Yes -> child=2

Result: 2 children satisfied
(Child with greed=3 can't be satisfied -- no cookie left)
```

### Example 3: Lemonade Change (LC 860)

**Why greedy works:** When making $15 change for a $20 bill, prefer $10+$5 over $5+$5+$5. The $5 bill is more **versatile** -- it can make change for both $10 and $20 bills, while a $10 bill only helps with $20. Conserving the more flexible denomination is the greedy insight.

```python
def lemonade_change(bills: list[int]) -> bool:
    """
    Give correct change for $5 lemonade. Bills can be $5, $10, or $20.

    Greedy strategy: When making $15 change, prefer $10+$5 over $5+$5+$5.
    The $5 bill is more versatile -- it makes change for both $10 and $20 bills.

    Time:  O(n) -- single pass through bills
    Space: O(1) -- only two counters
    """
    fives = 0
    tens = 0

    for bill in bills:
        if bill == 5:
            fives += 1
        elif bill == 10:
            if fives == 0:
                return False
            fives -= 1
            tens += 1
        else:  # bill == 20, need $15 change
            if tens > 0 and fives > 0:
                # Prefer $10+$5: conserves versatile $5 bills
                tens -= 1
                fives -= 1
            elif fives >= 3:
                fives -= 3
            else:
                return False

    return True
```

**Visual trace:**

```text
bills = [5, 5, 5, 10, 20]

bill=5:  fives=1, tens=0  (no change needed)
bill=5:  fives=2, tens=0  (no change needed)
bill=5:  fives=3, tens=0  (no change needed)
bill=10: fives=2, tens=1  (gave back $5)
bill=20: fives=1, tens=0  (gave back $10+$5, greedy choice!)

Result: True -- all customers got correct change
```

---

## Greedy vs DP

Both greedy and DP solve optimization problems with **optimal substructure** (an optimal solution contains optimal sub-solutions). They differ in how they make choices:

| Feature | Greedy | Dynamic Programming |
| :--- | :--- | :--- |
| **Decision making** | Makes the locally best choice right now | Considers all possible choices by exploring subproblems |
| **Reversibility** | Irrevocable -- once a choice is made, it's never reconsidered | Explores many paths and chooses the global best |
| **Subproblems** | Only solves _one_ subproblem (the one remaining after the greedy choice) | Solves _all_ overlapping subproblems |
| **Performance** | Usually faster: $O(n \log n)$ or $O(n)$ | Usually slower: $O(n^2)$ or $O(n \cdot W)$, and uses more memory |
| **Key requirement** | **Greedy choice property** -- local optimum is always safe to commit to | **Overlapping subproblems** -- same subproblems recur, so memoization pays off |

### Decision Tree

```text
Does the problem have Optimal Substructure?
    |
    +-- No --> Neither Greedy nor DP applies
    |
    +-- Yes
        |
        +-- Can you prove the Greedy Choice Property?
            +-- Yes --> Use Greedy (verify with counter-examples first)
            +-- No / Unsure
                |
                +-- Are there overlapping subproblems?
                    +-- Yes --> Use DP
                    +-- No  --> Divide & Conquer (or reconsider Greedy)
```

---

## Common Greedy Patterns

| Pattern | Strategy | Examples |
| --- | --- | --- |
| **Sorting first** | Sort by key attribute, then iterate | Activity selection, meeting rooms |
| **Two pointers** | Greedy matching from both ends | Assign cookies, boats to save people |
| **Track reachability** | Maintain what's achievable so far | Jump game, gas station |
| **Two pass** | Forward pass + backward pass | Candy distribution |
| **Heap-based** | Always process min/max first | Task scheduler, Huffman coding |

---

## Complexity Analysis

| Operation | Time | Space | Notes |
| --- | --- | --- | --- |
| Sort-based greedy | $O(n \log n)$ | $O(n)$ | Sorting dominates; $O(n)$ for sorted copy (Python's `sorted()`) |
| Single pass | $O(n)$ | $O(1)$ | Linear scan with constant extra variables |
| Two pass | $O(n)$ | $O(n)$ | Forward + backward, typically needs auxiliary array |
| Heap-based | $O(n \log n)$ | $O(n)$ | Each of n elements inserted/extracted from heap |
| In-place sort | $O(n \log n)$ | $O(n)$ | Using `.sort()` mutates input but saves the overhead of creating a new list (Timsort still uses $O(n)$ auxiliary space) |

**Note on Python sorting:**
- `list.sort()` - sorts in-place and **mutates the input**. (Note: Python's Timsort algorithm technically requires $O(n)$ auxiliary space in the worst case, but it avoids creating a full copy of the list).
- `sorted(list)` - returns a new sorted list, requiring $O(n)$ space for the copy, and **preserves the input**.

In interviews, prefer `sorted()` unless told otherwise, to avoid side effects.

---

## Edge Cases

| Edge Case | Why It Matters | Example |
| --- | --- | --- |
| Empty input | Usually return 0, empty list, or base case | `activity_selection([])` → `[]` |
| Single element | Often the answer itself | One activity → select it |
| All same values | Ties need consistent handling | All activities have same end time |
| Already sorted | Algorithm should still work | Input already in greedy order |
| Reverse sorted | Sorting must handle correctly | Activities sorted by start time |
| All elements same | No distinct "best" choice | All cookies same size |
| Zero values | Division by zero, infinite loops | Zero-weight items in knapsack |
| Negative values | May break greedy criterion | Negative profits/weights |
| Ties in ordering | Must handle consistently | Multiple activities end at same time |

**Testing checklist:**
- [ ] Trace through with empty input
- [ ] Trace through with single element
- [ ] Create a counter-example to your greedy strategy
- [ ] Test with all identical values
- [ ] Test boundary conditions (exactly at capacity/limit)

---

## Practice Problems

Problems are ordered easy to medium. Assign Cookies and Lemonade Change are solved above in [Classic Greedy Problems](#classic-greedy-problems).

### Problem 1: Minimum Sum of Four Digit Number After Splitting Digits (LC 2160) -- Easy

**Problem:** You are given a positive integer `num` consisting of exactly four digits. Split `num` into two new integers `new1` and `new2` by using the digits found in `num`. Leading zeros are allowed, and all digits must be used. Return the minimum possible sum of `new1` and `new2`.

**Greedy insight:** To minimize the sum of two numbers formed by four digits, we should place the two smallest digits in the tens place, and the two largest digits in the ones place.

```python
def minimum_sum(num: int) -> int:
    """
    Time:  O(1) -- sorting 4 digits takes constant time
    Space: O(1) -- space for 4 digits is constant
    """
    # Convert number to list of its digits and sort them
    digits = sorted(int(d) for d in str(num))

    # Form the two numbers:
    # Smallest digits go to the tens place, largest to the ones place
    new1 = digits[0] * 10 + digits[2]
    new2 = digits[1] * 10 + digits[3]

    return new1 + new2
```

**Why greedy works:** The value of a digit in the tens place is multiplied by 10, while in the ones place it's multiplied by 1. To minimize the total sum, we must assign the smallest possible multiplier (10 instead of 100 or 1000) to the digits. By splitting the four digits into two two-digit numbers, we avoid creating any hundreds or thousands place. Then, we place the two absolutely smallest digits in the tens place to minimize their impact.

---

### Problem 2: Maximum Units on a Truck (LC 1710) -- Easy

**Problem:** You have `box_types[i] = [count, units_per_box]`. Load a truck with at most `truck_size` boxes. Maximize total units.

**Greedy insight:** Load boxes with the most units first. Since every box takes the same space (1 slot), there is no trade-off -- higher units per box is strictly better.

```python
def maximum_units(box_types: list[list[int]], truck_size: int) -> int:
    """
    Time:  O(n log n) -- sorting by units per box
    Space: O(n) -- for the sorted copy
    """
    # Sort by units per box, descending (most valuable boxes first)
    sorted_boxes = sorted(box_types, key=lambda x: x[1], reverse=True)

    total_units = 0
    remaining_space = truck_size

    for count, units in sorted_boxes:
        boxes_to_load = min(count, remaining_space)
        total_units += boxes_to_load * units
        remaining_space -= boxes_to_load
        if remaining_space == 0:
            break

    return total_units
```

**Visual trace:**

```text
box_types = [[1,3], [2,2], [3,1]], truck_size = 4

Sorted by units/box (desc): [[1,3], [2,2], [3,1]]

Load [1,3]: take 1 box, +3 units  (space left: 3)
Load [2,2]: take 2 boxes, +4 units (space left: 1)
Load [3,1]: take 1 box, +1 unit   (space left: 0, full!)

Total: 3 + 4 + 1 = 8 units
```

**Why greedy works:** Every box occupies exactly one slot. There is no blocking -- a box with more units is always better than one with fewer, regardless of what else you load. This gives us the greedy choice property trivially.

---

### Problem 3: Best Time to Buy and Sell Stock II (LC 122) -- Medium

**Problem:** Given daily stock prices, find maximum profit. You may buy and sell multiple times (but must sell before buying again).

**Greedy insight:** Collect every upward price movement. If `prices[i+1] > prices[i]`, that delta is free profit. You don't need to track buy/sell pairs explicitly.

```python
def max_profit(prices: list[int]) -> int:
    """
    Time:  O(n) -- single pass
    Space: O(1)
    """
    profit = 0
    # Every time the price goes up, we 'buy' yesterday and 'sell' today
    for i in range(1, len(prices)):
        if prices[i] > prices[i - 1]:
            profit += prices[i] - prices[i - 1]
    return profit
```

**Visual trace:**

```text
prices = [7, 1, 5, 3, 6, 4]

Day 0->1: 1 - 7 = -6 (skip, negative)
Day 1->2: 5 - 1 = +4  (collect!)
Day 2->3: 3 - 5 = -2  (skip, negative)
Day 3->4: 6 - 3 = +3  (collect!)
Day 4->5: 4 - 6 = -2  (skip, negative)

Total profit: 4 + 3 = 7
Equivalent to: buy at 1, sell at 5 (+4), buy at 3, sell at 6 (+3)
```

**Why greedy works:** Any multi-day profit (buy at day $a$, sell at day $b$) equals the sum of consecutive daily gains between $a$ and $b$. So collecting all positive deltas captures every profitable opportunity without missing any. There is no blocking because we can trade every day.

---

### Problem 3: Boats to Save People (LC 881) -- Medium

**Problem:** People have weights. Each boat holds at most 2 people and has a weight `limit`. Find the minimum number of boats.

**Greedy insight:** Pair the lightest and heaviest person. If they fit together, great -- we saved a boat. If not, the heaviest person must ride alone (nobody else can pair with them either). Two pointers after sorting.

```python
def num_rescue_boats(people: list[int], limit: int) -> int:
    """
    Time:  O(n log n) -- sorting dominates
    Space: O(n) -- for the sorted copy
    """
    sorted_people = sorted(people)
    left, right = 0, len(sorted_people) - 1
    boats = 0

    while left <= right:
        # Try to pair the lightest person with the heaviest person
        if sorted_people[left] + sorted_people[right] <= limit:
            left += 1  # Lightest person pairs with heaviest
        right -= 1     # Heaviest person boards (alone or paired)
        boats += 1

    return boats
```

**Visual trace:**

```text
people = [3, 2, 2, 1], limit = 3

Sorted: [1, 2, 2, 3]
         L           R

Step 1: 1 + 3 = 4 > 3  -> 3 rides alone, R-- (boats=1)
        [1, 2, 2, 3]
         L     R

Step 2: 1 + 2 = 3 <= 3 -> pair (1,2), L++, R-- (boats=2)
        [1, 2, 2, 3]
            LR

Step 3: 2 alone (L == R) -> R-- (boats=3)

Result: 3 boats
```

**Why greedy works (exchange argument):** If the heaviest person can pair with the lightest, pairing them is optimal -- using the lightest person is the "cheapest" way to fill the second seat. If they can't pair, the heaviest person can't pair with anyone (since everyone else weighs at least as much as the lightest), so they must ride alone.

---

### More Practice

| # | Problem | Difficulty | Key Insight |
| --- | --- | --- | --- |
| 1 | Assign Cookies (LC 455) | Easy | Sort both, greedy matching |
| 2 | Lemonade Change (LC 860) | Easy | Greedy change giving, conserve versatile bills |
| 3 | Maximum Units on a Truck (LC 1710) | Easy | Sort by value, fill greedily |
| 4 | Best Time to Buy and Sell Stock II (LC 122) | Medium | Collect all positive deltas |
| 5 | Boats to Save People (LC 881) | Medium | Two-pointer greedy pairing |
| 6 | Minimum Number of Arrows to Burst Balloons (LC 452) | Medium | Interval greedy (covered in later notes) |

---

## Interview Tips

1. **State the greedy strategy clearly**: "I'll sort by X and greedily pick Y"
2. **Justify why it works**: Argue greedy choice property, ideally via exchange argument
3. **Consider counter-examples**: Think about when greedy might fail
4. **Compare to DP**: Explain why DP isn't needed (or is)
5. **Verify with examples**: Trace through the algorithm manually

---

## Recognizing Greedy Problems

**Clues that greedy might work:**

1. **Optimization problem** - minimizing or maximizing something
2. **Sequential decisions** - you make choices one after another
3. **Natural ordering** - there's an obvious way to sort or prioritize
4. **"Take what you can"** - the problem suggests accumulating or selecting greedily
5. **No looking back** - previous choices don't need to be revisited

**Common problem types:**

| Problem Type | Greedy Criterion | Why It Works |
| --- | --- | --- |
| Interval scheduling / activity selection | Earliest end time | Maximizes remaining time for other intervals |
| Fractional knapsack | Value/weight ratio | Best marginal gain per unit capacity |
| Huffman coding | Lowest frequency | Minimizes weighted path length |
| Minimum spanning tree | Minimum edge weight | Cut property guarantees optimality |
| Jump game | Maximum reachable index | Contiguous reachability -- only frontier matters |

---

## Key Takeaways

1. Greedy makes locally optimal choices aiming for the global optimum
2. Requires both **greedy choice property** and **optimal substructure**
3. Three proof techniques: **stays ahead**, **exchange argument**, **contradiction**
4. Faster than DP but only correct when greedy choice property holds
5. **Counter-examples** are the fastest way to disprove greedy applicability
6. When greedy fails, consider: DP, backtracking, or approximation algorithms
7. For **maximization problems**, think: "What choice leaves the most room for others?"
8. For **minimization problems**, think: "What choice contributes least to the cost?"

---

## Next: [02-interval-scheduling.md](./02-interval-scheduling.md)

Learn the classic interval scheduling pattern: activity selection and maximum meetings.
