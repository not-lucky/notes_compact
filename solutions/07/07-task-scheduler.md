# Task Scheduler

## Practice Problems

### 1. Task Scheduler
**Difficulty:** Medium
**Concept:** Greedy + Max Heap + Cooldown Queue

```python
import heapq
from collections import Counter, deque
from typing import List

def least_interval(tasks: List[str], n: int) -> int:
    """
    Calculate minimum intervals to complete all tasks with cooldown n.

    >>> least_interval(["A","A","A","B","B","B"], 2)
    8
    >>> least_interval(["A","A","A","B","B","B"], 0)
    6

    Time: O(T log U) where T is total tasks, U is unique tasks
    Space: O(U)
    """
    counts = Counter(tasks)
    max_heap = [-cnt for cnt in counts.values()]
    heapq.heapify(max_heap)

    time = 0
    queue = deque()  # stores (rem_cnt, available_time)

    while max_heap or queue:
        time += 1
        if max_heap:
            cnt = 1 + heapq.heappop(max_heap)  # execute one instance
            if cnt < 0:
                queue.append((cnt, time + n))

        if queue and queue[0][1] == time:
            heapq.heappush(max_heap, queue.popleft()[0])

    return time
```
