# Task Scheduler

> **Prerequisites:** [02-python-heapq](./02-python-heapq.md), [03-top-k-pattern](./03-top-k-pattern.md)

## Interview Context

Task scheduling problems are FANG+ favorites because:

1. **Real-world relevance**: CPU scheduling, job queues, rate limiting
2. **Greedy + Heap**: Shows understanding of greedy strategies
3. **Cooldown constraint**: Adds complexity beyond basic heap
4. **Multiple valid approaches**: Heap, formula, simulation

This problem appears frequently at Facebook and Amazon interviews.

---

## Problem Statement

Given a list of tasks represented by characters and a cooling interval `n`, return the minimum time needed to complete all tasks.

**Constraint**: Same tasks must be separated by at least `n` intervals.

```
Example 1:
tasks = ["A","A","A","B","B","B"], n = 2
Output: 8

Execution: A → B → idle → A → B → idle → A → B
           1   2    3     4   5    6     7   8

Example 2:
tasks = ["A","A","A","B","B","B"], n = 0
Output: 6 (no cooling needed, just do all tasks)
```

---

## Core Insight

**Greedy Strategy**: Always execute the task with highest remaining count that's not on cooldown.

Why? High-frequency tasks are the bottleneck. If we don't prioritize them, we'll have more idle slots at the end.

---

## Approach 1: Max Heap + Cooldown Queue

```python
import heapq
from collections import Counter, deque

def least_interval(tasks: list[str], n: int) -> int:
    """
    Calculate minimum intervals to complete all tasks.

    Time: O(total_tasks * log(unique_tasks))
    Space: O(unique_tasks)

    Strategy: Max heap for counts, queue for cooldown.
    """
    # Count task frequencies
    count = Counter(tasks)

    # Max heap of remaining counts (negate for max heap)
    max_heap = [-cnt for cnt in count.values()]
    heapq.heapify(max_heap)

    # Queue of (remaining_count, available_time)
    cooldown = deque()

    time = 0

    while max_heap or cooldown:
        time += 1

        if max_heap:
            # Execute task with highest remaining count
            remaining = heapq.heappop(max_heap) + 1  # +1 because negated

            if remaining < 0:  # Still has tasks left
                cooldown.append((remaining, time + n))
        # else: idle (nothing to execute)

        # Check if any task finished cooldown
        if cooldown and cooldown[0][1] == time:
            heapq.heappush(max_heap, cooldown.popleft()[0])

    return time


# Usage
tasks = ["A", "A", "A", "B", "B", "B"]
print(least_interval(tasks, 2))  # 8
```

---

## Visual Walkthrough

```
tasks = ["A","A","A","B","B","B"], n = 2

Initial: max_heap = [-3, -3]  (A:3, B:3)
         cooldown = []

Time 1: Pop A(-3→-2), cooldown = [(-2, 3)]
        heap = [-3(B)]
        Execute: A

Time 2: Pop B(-3→-2), cooldown = [(-2, 3), (-2, 4)]
        heap = []
        Execute: B

Time 3: heap empty, idle
        cooldown[0] available at time 3 → push -2(A) to heap
        cooldown = [(-2, 4)]
        Execute: idle

Time 4: Pop A(-2→-1), cooldown = [(-2, 4), (-1, 6)]
        heap = []
        Check: cooldown[0] available at time 4 → push -2(B)
        Execute: A

Time 5: Pop B(-2→-1), cooldown = [(-1, 6), (-1, 7)]
        Execute: B

Time 6: heap empty
        cooldown[0] available → push -1(A)
        Pop A(-1→0), done with A
        Execute: A

Time 7: heap empty
        cooldown[0] available → push -1(B)
        Pop B(-1→0), done with B
        Execute: B

Time 8: cooldown empty, heap empty
        Wait, we need to check...

Actually final: 8 intervals
A → B → idle → A → B → idle → A → B
```

---

## Approach 2: Formula (O(1) Space)

```python
from collections import Counter

def least_interval_formula(tasks: list[str], n: int) -> int:
    """
    Calculate using mathematical formula.

    Time: O(tasks)
    Space: O(26) = O(1)

    Key insight: The task with max frequency determines minimum time.
    """
    count = Counter(tasks)
    max_count = max(count.values())

    # How many tasks have the max count?
    num_max = sum(1 for c in count.values() if c == max_count)

    # Formula: (max_count - 1) * (n + 1) + num_max
    # Explanation:
    # - We need (max_count - 1) complete cycles of (n + 1) slots
    # - Plus one final round of tasks with max_count

    result = (max_count - 1) * (n + 1) + num_max

    # But if we have many different tasks, we might not need idle slots
    return max(result, len(tasks))


# Visual for tasks = [A,A,A,B,B,B], n = 2, max_count = 3, num_max = 2
#
# A _ _ | A _ _ | A     (max_count - 1 = 2 complete cycles)
# A B _ | A B _ | A B   (fill with B)
#
# Formula: (3-1) * (2+1) + 2 = 2 * 3 + 2 = 8 ✓
```

---

## Why the Formula Works

```
For tasks = [A,A,A,A,B,B,C,C], n = 2

max_count = 4 (A appears 4 times)
num_max = 1 (only A has max count)

Minimum slots: (4-1) * (2+1) + 1 = 10

Layout:
A _ _ | A _ _ | A _ _ | A
A B C | A B C | A _ _ | A    (fill with B, C)

Still 10 slots (idle at position 9)

But if we had more tasks:
tasks = [A,A,A,A,B,B,B,B,C,C,D,D,E,E,F], n = 2
num_max = 2 (A and B both have 4)

Layout needed:
A B _ | A B _ | A B _ | A B   = (4-1)*3 + 2 = 11

But we have 15 tasks! And 11 slots isn't enough.
So return max(11, 15) = 15

Actually with many tasks, no idle needed:
A B C D E A B C D F A B ... (all filled)
```

---

## Approach 3: Simulation with Round-Robin

```python
from collections import Counter

def least_interval_simulation(tasks: list[str], n: int) -> int:
    """
    Simulate round-robin execution.

    Time: O(total_time * unique_tasks)
    Space: O(unique_tasks)
    """
    count = Counter(tasks)
    counts = sorted(count.values(), reverse=True)

    time = 0

    while counts[0] > 0:
        # Try to fill one cycle of n+1 slots
        for i in range(n + 1):
            if counts[0] == 0:
                break

            time += 1

            # Execute task i if it exists and has remaining
            if i < len(counts) and counts[i] > 0:
                counts[i] -= 1

        # Re-sort for next round
        counts.sort(reverse=True)

    return time
```

Less efficient but easier to understand.

---

## Comparison of Approaches

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Heap + Queue | O(T log U) | O(U) | Most intuitive |
| Formula | O(T) | O(1) | Fastest |
| Simulation | O(T * U) | O(U) | Simple but slow |

T = total tasks, U = unique tasks (≤ 26)

---

## Related: Task Scheduler II

Different variant where each task has execution time:

```python
import heapq

def task_scheduler_ii(tasks: list[int], space: int) -> int:
    """
    Each task type needs 'space' gap between executions.

    Time: O(n)
    Space: O(n)
    """
    last_executed = {}  # task_type -> last execution day
    day = 0

    for task in tasks:
        day += 1

        if task in last_executed:
            # Must wait until cooldown ends
            min_day = last_executed[task] + space + 1
            day = max(day, min_day)

        last_executed[task] = day

    return day
```

---

## Related: Reorganize String

Related problem: Rearrange string so no two adjacent chars are same.

```python
import heapq
from collections import Counter

def reorganize_string(s: str) -> str:
    """
    Rearrange so no adjacent characters are same.

    Time: O(n log k) where k = unique chars
    Space: O(k)
    """
    count = Counter(s)

    # If any char appears more than (n+1)/2 times, impossible
    max_count = max(count.values())
    if max_count > (len(s) + 1) // 2:
        return ""

    # Max heap of (-count, char)
    max_heap = [(-cnt, char) for char, cnt in count.items()]
    heapq.heapify(max_heap)

    result = []
    prev = (0, '')  # Previous char (cooldown of 1)

    while max_heap:
        cnt, char = heapq.heappop(max_heap)
        result.append(char)

        # Push previous back (if still has count)
        if prev[0] < 0:
            heapq.heappush(max_heap, prev)

        prev = (cnt + 1, char)  # Current becomes previous

    return ''.join(result)
```

---

## Edge Cases

```python
# 1. No cooldown needed (n = 0)
least_interval(["A", "A", "B"], 0)  # 3

# 2. Single task type
least_interval(["A", "A", "A"], 2)
# A _ _ A _ _ A = 7

# 3. Many task types, short cooldown
least_interval(["A", "B", "C", "D", "E", "F"], 1)  # 6 (no idle)

# 4. All same task
least_interval(["A", "A", "A", "A"], 3)
# A _ _ _ A _ _ _ A _ _ _ A = 13

# 5. n larger than unique tasks
least_interval(["A", "B", "A", "B"], 3)
# A B _ _ A B = 6
```

---

## Common Mistakes

```python
# WRONG: Not using max heap
count = Counter(tasks)
for task in sorted(count, key=count.get):  # Min frequency first!
    ...

# CORRECT: Max heap or sorted by -count


# WRONG: Forgetting to check cooldown
while max_heap:
    task = heapq.heappop(max_heap)
    # Execute... but what if still on cooldown?

# CORRECT: Use cooldown queue


# WRONG: Off-by-one in formula
result = max_count * (n + 1)  # Wrong!

# CORRECT:
result = (max_count - 1) * (n + 1) + num_max
```

---

## Interview Tips

1. **Explain greedy choice**: Why prioritize highest frequency?
2. **Know both approaches**: Heap for simulation, formula for efficiency
3. **Walk through example**: Show cooldown queue state changes
4. **Discuss edge cases**: n=0, single task type, many task types
5. **Mention formula**: Shows mathematical thinking

---

## Practice Problems

| # | Problem | Difficulty | Key Variation |
|---|---------|------------|---------------|
| 1 | Task Scheduler | Medium | Core problem |
| 2 | Reorganize String | Medium | Cooldown of 1 |
| 3 | Task Scheduler II | Medium | Different formulation |
| 4 | Distant Barcodes | Medium | Reorganize array |
| 5 | Course Schedule III | Hard | Heap + greedy |

---

## Key Takeaways

1. **Greedy strategy**: Always do highest-frequency task not on cooldown
2. **Max heap + cooldown queue**: Track remaining counts and availability
3. **Formula approach**: (max_count - 1) * (n + 1) + num_max
4. **Must take max**: Result could be just len(tasks) if many unique tasks
5. **Related patterns**: Reorganize string, distant barcodes

---

## Next: [08-k-closest-points.md](./08-k-closest-points.md)

Learn heap problems involving distance calculations.
