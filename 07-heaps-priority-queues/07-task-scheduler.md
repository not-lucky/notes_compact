# Task Scheduler

> **Prerequisites:** [02-python-heapq](./02-python-heapq.md), [03-top-k-pattern](./03-top-k-pattern.md)

## Interview Context

Task scheduling problems are FANG+ favorites because:

1. **Real-world relevance**: CPU scheduling, job queues, rate limiting.
2. **Greedy + Heap**: Demonstrates understanding of greedy strategies implemented via max-heaps.
3. **Cooldown constraint**: Adds state management complexity beyond basic heap usage.
4. **Multiple valid approaches**: Simulation (heap) vs. Math (formula).

This problem (Leetcode 621) appears very frequently at Meta (Facebook) and Amazon interviews.

---

## The Problem Statement

Given a list of `tasks` represented by characters and a cooling interval `n`, return the minimum time needed to complete all tasks.

**Constraint**: Identical tasks must be separated by at least `n` intervals. If no tasks can be executed, the CPU remains idle.

### Examples

**Example 1:**
```
Input: tasks = ["A","A","A","B","B","B"], n = 2
Output: 8
Explanation: A -> B -> idle -> A -> B -> idle -> A -> B
             1    2     3      4    5     6      7    8
```

**Example 2:**
```
Input: tasks = ["A","C","A","B","D","B"], n = 1
Output: 6
Explanation: A -> B -> C -> D -> A -> B (No idles needed)
```

---

## Building Intuition

### The Core Problem: Managing Cooldowns

Tasks of the same type need separation. This creates "slots" that may be empty:

```
Tasks: [A, A, A], cooldown n = 2

Without cooldown: A A A (3 units)
With cooldown:    A _ _ A _ _ A (7 units)
                    ^-^   ^-^
                  2 slots between each A
```

### Why Prioritize High-Frequency Tasks?

High-frequency tasks are the bottleneck. If you don't handle them first, you'll be forced to insert more idles at the end.

**Key Insight:** Always execute the most frequent available task. This is a **Greedy Strategy**.

```
Tasks: [A, A, A, B], n = 2

Bad order (B first):
B A _ _ A _ _ A  = 8 units (2 idles)

Good order (A first):
A B _ A _ _ A    = 7 units (2 idles)
```

### Mental Model: The Radio Station

Imagine a DJ with a stack of song requests who cannot repeat a song within `n` tracks:
- Prioritize the most-requested songs.
- After playing a song, it goes on a "cooldown" for `n` tracks.
- If no song is available, play an ad (idle).

---

## Approach 1: Max-Heap + Cooldown Queue (Simulation)

This approach simulates the execution of tasks tick by tick.

### Data Structures Needed
1. **Max-Heap**: Tracks the remaining frequencies of *available* tasks.
2. **Cooldown Queue**: A `deque` storing `(remaining_count, available_time)`. This tracks tasks currently on cooldown.

### Algorithm
At each time step:
1. Increment the `time`.
2. **Execute**: If the heap has available tasks, pop the one with the highest frequency, decrement its count, and if it still has remaining executions, push it to the cooldown queue with `available_time = time + n`.
3. **Restore**: Check if the task at the front of the cooldown queue has finished its cooldown (`available_time == time`). If so, move it back to the max-heap.
4. If both heap and queue are empty, we are done.

### Python Implementation

```python
import heapq
from collections import Counter, deque

def least_interval(tasks: list[str], n: int) -> int:
    """
    Time: O(T * log U) where T = total tasks, U = unique tasks
    Space: O(U)
    Note: Since U <= 26 (uppercase English letters), Time is effectively O(T) and Space is O(1).
    """
    # 1. Count frequencies
    count = Counter(tasks)

    # 2. Max heap of remaining counts (Python has min-heap, so negate values)
    max_heap = [-cnt for cnt in count.values()]
    heapq.heapify(max_heap)

    time = 0
    # Queue stores: (remaining_count, available_time)
    cooldown = deque()

    # Continue while we have tasks available or on cooldown
    while max_heap or cooldown:
        time += 1

        # If tasks are available, execute the most frequent one
        if max_heap:
            # Pop and increment (since values are negative)
            remaining = heapq.heappop(max_heap) + 1

            # If still tasks left of this type, put on cooldown
            if remaining < 0:
                cooldown.append((remaining, time + n))

        # Check if any task finished cooldown at current time
        if cooldown and cooldown[0][1] == time:
            # Move back to heap
            heapq.heappush(max_heap, cooldown.popleft()[0])

    return time
```

### Visual Walkthrough

```
tasks = ["A","A","A","B","B","B"], n = 2

Initial: max_heap = [-3(A), -3(B)]
         cooldown = []

Time 1: Pop A(-3->-2), cooldown = [(-2, 3)]
        heap = [-3(B)]
        Schedule: A

Time 2: Pop B(-3->-2), cooldown = [(-2, 3), (-2, 4)]
        heap = []
        Schedule: B

Time 3: heap empty, idle
        Restore A: cooldown[0] available at 3 -> push -2(A) to heap
        cooldown = [(-2, 4)]
        Schedule: idle

Time 4: Pop A(-2->-1), cooldown = [(-2, 4), (-1, 6)]
        Restore B: cooldown[0] available at 4 -> push -2(B) to heap
        heap = [-2(B)]
        Schedule: A

Time 5: Pop B(-2->-1), cooldown = [(-1, 6), (-1, 7)]
        heap = []
        Schedule: B

Time 6: heap empty, idle
        Restore A: cooldown[0] available at 6 -> push -1(A)
        Schedule: idle

Time 7: Pop A(-1->0), done with A
        Restore B: cooldown[0] available at 7 -> push -1(B)
        Schedule: A

Time 8: Pop B(-1->0), done with B
        cooldown empty, heap empty -> Break.
        Schedule: B

Final time: 8
```

---

## Approach 2: The Mathematical Formula (O(1) Space)

If you only need the *minimum time* (and not the actual schedule), you can use a formula based on the most frequent task(s).

### Key Insights
1. The most frequent task acts as a "frame".
2. If we arrange the most frequent task `A` (count = 3) with `n = 2`:
   `A _ _ | A _ _ | A`
3. We have `(max_count - 1)` complete cycles. Each cycle has length `(n + 1)`.
4. The final cycle just contains the tasks that are tied for the maximum frequency.

### The Formula
`result = (max_count - 1) * (n + 1) + num_max`

Where:
- `max_count` = frequency of the most common task(s)
- `num_max` = number of different tasks that appear `max_count` times

**Wait, what if the formula gives a number smaller than `len(tasks)`?**
This happens when there are many different tasks and `n` is small. We don't need any idles! Every slot naturally fills up, and we just process tasks without waiting. In this case, the answer is just `len(tasks)`.

Thus: `return max(result, len(tasks))`

### Python Implementation

```python
from collections import Counter

def least_interval_formula(tasks: list[str], n: int) -> int:
    """
    Time: O(T) where T = total tasks
    Space: O(1) (Counter takes at most 26 elements)
    """
    # Quick exit
    if n == 0:
        return len(tasks)

    count = Counter(tasks)
    max_count = max(count.values())

    # Count how many tasks share the maximum frequency
    num_max = sum(1 for c in count.values() if c == max_count)

    # Calculate intervals using the formula
    intervals = (max_count - 1) * (n + 1) + num_max

    # If intervals < len(tasks), it means we have enough distinct tasks
    # to fill all cooldown gaps without any idle time.
    return max(intervals, len(tasks))
```

### Visualizing the Formula

```
Tasks: [A,A,A,A, B,B,B,B, C,C, D, E], n = 2
max_count = 4 (for A and B)
num_max = 2 (A and B)

Formula: (4 - 1) * (2 + 1) + 2 = 3 * 3 + 2 = 11
Layout framework:
A B _ | A B _ | A B _ | A B

Fill in the blanks with C, C, D, E:
A B C | A B C | A B D | A B E
Wait, we have 12 tasks total, but formula gave 11!
Since 12 > 11, we return max(11, 12) = 12. No idles needed.
```

---

## When to Use Which Approach

**Use Max-Heap Simulation when:**
1. The interviewer asks for the **actual execution order** (e.g., returning the string `"AB_AB_AB"`).
2. The cooldown rule changes dynamically.
3. You need to prove the logic constructively.

**Use the Formula when:**
1. You only need the **minimum time** (integer).
2. You want the most optimal O(N) time, O(1) space solution.

> **Interview Tip:** Always explain the Heap simulation first to prove you understand the greedy logic, then offer the Formula as an O(N) optimization!

---

## Related Problems

### 1. Reorganize String (Leetcode 767)
**Problem:** Rearrange a string so no two adjacent characters are the same.
**Relation:** This is exactly Task Scheduler with `n = 1`, but you must return the actual string.

```python
import heapq
from collections import Counter

def reorganizeString(s: str) -> str:
    count = Counter(s)
    # Impossible if a char appears more than half the time (rounded up)
    if max(count.values()) > (len(s) + 1) // 2:
        return ""

    max_heap = [(-cnt, char) for char, cnt in count.items()]
    heapq.heapify(max_heap)

    res = []
    # Cooldown queue of size 1, stores: (count, char)
    prev = None

    while max_heap or prev:
        if prev and not max_heap:
            return "" # Failed to reorganize

        cnt, char = heapq.heappop(max_heap)
        res.append(char)
        cnt += 1 # Decrement magnitude

        # If previous character still has count, it's off cooldown now
        if prev:
            heapq.heappush(max_heap, prev)
            prev = None

        # Put current char on cooldown if it still has count
        if cnt < 0:
            prev = (cnt, char)

    return "".join(res)
```

### 2. Task Scheduler II (Leetcode 2365)
**Problem:** Tasks must be executed in the given order. Same tasks must have `space` days between them.
**Relation:** You CANNOT reorder tasks. No heap needed. Just use a Hash Map to track the next available day for each task type.

```python
def taskSchedulerII(tasks: list[int], space: int) -> int:
    available_day = {} # task_type -> earliest day it can run
    day = 0

    for task in tasks:
        day += 1
        # If task is on cooldown, fast-forward time
        if task in available_day and day < available_day[task]:
            day = available_day[task]

        # Update when this task can run next
        available_day[task] = day + space + 1

    return day
```

---

## Edge Cases to Consider

1. **`n = 0` (No cooldown)**: Just return `len(tasks)`.
2. **All tasks are identical**: Heaviest reliance on idles `(count - 1) * (n + 1) + 1`.
3. **Many unique tasks**: Cooldowns naturally fill up, resulting in `len(tasks)`.
4. **`n` is very large**: Handled flawlessly by both heap and formula.

---

## Common Mistakes

1. **Forgetting to put the heap item back**: In simulation, remembering to push tasks back to the heap once they exit the cooldown queue.
2. **Formula off-by-one**: Forgetting the `+ num_max` at the end of the formula, or forgetting `(n + 1)` instead of just `n`.
3. **Not using `max(result, len(tasks))`**: The formula can undercount if there are many distinct tasks filling the gaps.

---

## Practice Problems

| Problem | Difficulty | Key Variation |
| ------- | ---------- | ------------- |
| [Task Scheduler](https://leetcode.com/problems/task-scheduler/) | Medium | Core problem (Return count) |
| [Reorganize String](https://leetcode.com/problems/reorganize-string/) | Medium | `n = 1`, return actual schedule |
| [Task Scheduler II](https://leetcode.com/problems/task-scheduler-ii/) | Medium | Cannot reorder, track days |
| [Distant Barcodes](https://leetcode.com/problems/distant-barcodes/) | Medium | Reorganize array, return array |

---

## Next: [08-k-closest-points.md](./08-k-closest-points.md)

Learn heap problems involving distance calculations.
