# Solution: Task Scheduler Practice Problems

## Problem 1: Task Scheduler
### Problem Statement
Given a characters array `tasks`, representing the tasks a CPU needs to do, where each letter represents a different task. Tasks could be done in any order. Each task is done in one unit of time. For each unit of time, the CPU could complete either one task or just be idle.

However, there is a non-negative integer `n` that represents the cooldown period between two same tasks (the same letter in the array), that is that there must be at least `n` units of time between any two same tasks.

Return the least number of units of time that the CPU will take to finish all the given tasks.

### Constraints
- `1 <= tasks.length <= 10^4`
- `tasks[i]` is upper-case English letter.
- `0 <= n <= 100`

### Example
Input: `tasks = ["A","A","A","B","B","B"], n = 2`
Output: `8`
Explanation: `A -> B -> idle -> A -> B -> idle -> A -> B`

### Python Implementation
```python
import heapq
from collections import Counter, deque

def leastInterval(tasks: list[str], n: int) -> int:
    """
    Time Complexity: O(total_tasks * log(unique_tasks))
    Space Complexity: O(unique_tasks)
    """
    count = Counter(tasks)
    max_heap = [-cnt for cnt in count.values()]
    heapq.heapify(max_heap)

    queue = deque() # (neg_count, available_time)
    time = 0

    while max_heap or queue:
        time += 1
        if max_heap:
            cnt = heapq.heappop(max_heap) + 1
            if cnt:
                queue.append((cnt, time + n))

        if queue and queue[0][1] == time:
            heapq.heappush(max_heap, queue.popleft()[0])

    return time
```

---

## Problem 2: Reorganize String
### Problem Statement
Given a string `s`, rearrange the characters of `s` so that any two adjacent characters are not the same.

Return any possible rearrangement of `s` or return `""` if not possible.

### Constraints
- `1 <= s.length <= 500`
- `s` consists of lowercase English letters.

### Example
Input: `s = "aab"`
Output: `"aba"`

### Python Implementation
```python
import heapq
from collections import Counter

def reorganizeString(s: str) -> str:
    """
    Time Complexity: O(n log k) where k is number of unique chars
    Space Complexity: O(k)
    """
    count = Counter(s)
    max_heap = [(-cnt, char) for char, cnt in count.items()]
    heapq.heapify(max_heap)

    res = []
    prev = None

    while max_heap or prev:
        if prev and not max_heap:
            return ""

        cnt, char = heapq.heappop(max_heap)
        res.append(char)
        cnt += 1

        if prev:
            heapq.heappush(max_heap, prev)
            prev = None

        if cnt != 0:
            prev = (cnt, char)

    return "".join(res)
```

---

## Problem 3: Task Scheduler II
### Problem Statement
You are given a 0-indexed array of positive integers `tasks`, representing tasks that need to be completed in order, where `tasks[i]` represents the type of the `i`th task.

You are also given a positive integer `space`, which represents the minimum number of days that must pass after the completion of a task before another task of the same type can be performed.

Each day, you can either complete the next task from `tasks` or take a break.

Return the minimum number of days needed to complete all tasks.

### Constraints
- `1 <= tasks.length <= 10^5`
- `1 <= tasks[i] <= 10^9`
- `1 <= space <= 10^9`

### Python Implementation
```python
def taskSchedulerII(tasks: list[int], space: int) -> int:
    """
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    last_done = {} # task_type -> day
    curr_day = 0

    for t in tasks:
        curr_day += 1
        if t in last_done:
            # Check if cooldown is active
            if curr_day - last_done[t] <= space:
                curr_day = last_done[t] + space + 1
        last_done[t] = curr_day

    return curr_day
```

---

## Problem 4: Distant Barcodes
### Problem Statement
In a warehouse, there is a row of barcodes, where the `i`th barcode is `barcodes[i]`.

Rearrange the barcodes so that no two adjacent barcodes are equal. You may return any answer, and it is guaranteed an answer exists.

### Python Implementation
```python
import heapq
from collections import Counter

def rearrangeBarcodes(barcodes: list[int]) -> list[int]:
    """
    Time Complexity: O(n log k)
    Space Complexity: O(k)
    """
    count = Counter(barcodes)
    max_heap = [(-cnt, val) for val, cnt in count.items()]
    heapq.heapify(max_heap)

    res = []
    prev = None

    while max_heap:
        cnt, val = heapq.heappop(max_heap)
        res.append(val)

        if prev:
            heapq.heappush(max_heap, prev)
            prev = None

        if cnt + 1 < 0:
            prev = (cnt + 1, val)

    return res
```

---

## Problem 5: Course Schedule III
### Problem Statement
There are `n` different online courses numbered from `1` to `n`. You are given an array `courses` where `courses[i] = [durationi, lastDayi]` indicate that the `i`th course should be taken continuously for `durationi` days and must be finished before or on `lastDayi`.

You will start on the `1`st day and you cannot take two or more courses simultaneously.

Return the maximum number of courses that you can take.

### Constraints
- `1 <= courses.length <= 10^4`
- `1 <= durationi, lastDayi <= 10^4`

### Python Implementation
```python
import heapq

def scheduleCourse(courses: list[list[int]]) -> int:
    """
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    """
    # Sort courses by deadline
    courses.sort(key=lambda x: x[1])
    max_heap = [] # Store durations of taken courses
    curr_time = 0

    for dur, end in courses:
        if curr_time + dur <= end:
            heapq.heappush(max_heap, -dur)
            curr_time += dur
        elif max_heap and -max_heap[0] > dur:
            # Replace longest duration course with current shorter course
            curr_time += dur + heapq.heappop(max_heap)
            heapq.heappush(max_heap, -dur)

    return len(max_heap)
```
