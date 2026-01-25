# Task Scheduler Solutions

## 1. Task Scheduler
Minimum time to complete tasks with a cooldown `n`.

### Examples & Edge Cases
- **Example**: `tasks = ["A","A","A","B","B","B"], n = 2` -> `8`
- **Edge Case: n = 0**: Returns `len(tasks)`.
- **Edge Case: Single task type**: `["A","A"], n = 2` -> `A _ _ A` (4 slots).

### Optimal Python Solution (Max-Heap + Queue)
```python
import heapq
from collections import Counter, deque

def leastInterval(tasks: list[str], n: int) -> int:
    """
    Greedy: Always perform the task with the highest remaining frequency
    that is not currently on cooldown.

    Time Complexity: O(total_tasks * log(unique_tasks))
    Space Complexity: O(unique_tasks)
    """
    # 1. Count frequencies
    counts = Counter(tasks)
    # 2. Max-heap of remaining counts (negated)
    max_heap = [-cnt for cnt in counts.values()]
    heapq.heapify(max_heap)

    # 3. Queue to track tasks on cooldown: (remaining_count, available_time)
    queue = deque()
    time = 0

    while max_heap or queue:
        time += 1

        if max_heap:
            # Execute the most frequent available task
            cnt = heapq.heappop(max_heap) + 1 # Use 1 instance
            if cnt != 0:
                # If tasks remain, put on cooldown
                queue.append((cnt, time + n))

        # Check if any task is done with its cooldown
        if queue and queue[0][1] == time:
            heapq.heappush(max_heap, queue.popleft()[0])

    return time
```

### Explanation
1.  **Greedy Strategy**: High-frequency tasks create the most constraints. By doing them as soon as they are available, we minimize the total number of idle slots.
2.  **Heap**: Keeps available tasks ordered by their remaining counts.
3.  **Queue**: Acts as the cooldown buffer. Tasks wait in the queue until `time` reaches their `available_time`.

### Complexity Analysis
- **Time Complexity**: $O(T \log U)$ where $T$ is the total number of tasks and $U$ is the number of unique tasks (max 26).
- **Space Complexity**: $O(U)$ to store the frequencies and the heap.

---

## 2. Reorganize String
Rearrange characters so that no two adjacent characters are the same.

### Examples & Edge Cases
- **Example**: `s = "aab"` -> `"aba"`
- **Example**: `s = "aaab"` -> `""` (impossible)
- **Edge Case: Single character**: `"a"` -> `"a"`.

### Optimal Python Solution
```python
import heapq
from collections import Counter

def reorganizeString(s: str) -> str:
    """
    Greedily pick the character with the highest remaining frequency,
    ensuring it's not the same as the one we just used.

    Time Complexity: O(n log k) where k is alphabet size
    Space Complexity: O(k)
    """
    counts = Counter(s)
    max_heap = [(-cnt, char) for char, cnt in counts.items()]
    heapq.heapify(max_heap)

    res = []
    # (prev_count, prev_char) stores the char we used in the previous step
    prev = None

    while max_heap or prev:
        # If we have a char on 'cooldown' but no other chars to use, it's impossible
        if prev and not max_heap:
            return ""

        cnt, char = heapq.heappop(max_heap)
        res.append(char)
        cnt += 1 # Decrement frequency (it was negated)

        # Push the previous character back into the heap now that it's no longer adjacent
        if prev:
            heapq.heappush(max_heap, prev)
            prev = None

        # If the current character still has instances left, it goes on 'cooldown'
        if cnt < 0:
            prev = (cnt, char)

    return "".join(res)
```

### Explanation
1.  **Greedy Choice**: We always use the most frequent character available that isn't the same as the last one used.
2.  **State Management**: We use a `prev` variable to temporarily hold a character so it's not picked twice in a row.

---

## 3. Task Scheduler II
Each task type needs `space` gap between executions. Tasks must be executed in the given order.

### Examples & Edge Cases
- **Example**: `tasks = [1,2,1,2,3,1], space = 3` -> `9`
- **Edge Case: space = 0**: Returns `len(tasks)`.

### Optimal Python Solution
```python
def taskSchedulerII(tasks: list[int], space: int) -> int:
    """
    Since order is fixed, we just need to track when each task type was last
    executed and fast-forward time if necessary.

    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    last_exec = {}
    curr_day = 0

    for t in tasks:
        curr_day += 1
        if t in last_exec:
            # Check if we need to wait for cooldown
            # gap = curr_day - last_exec[t] - 1
            # we need gap >= space => curr_day >= last_exec[t] + space + 1
            curr_day = max(curr_day, last_exec[t] + space + 1)

        last_exec[t] = curr_day

    return curr_day
```

### Explanation
- Unlike the first Task Scheduler, the **order is fixed**. We don't use a heap because we can't choose which task to do next. We simply simulate the timeline and jump forward when a cooldown requirement isn't met.

---

## 4. Distant Barcodes
Rearrange barcodes so that no two adjacent barcodes are equal.

### Optimal Python Solution
```python
import heapq
from collections import Counter

def rearrangeBarcodes(barcodes: list[int]) -> list[int]:
    """
    Identical logic to Reorganize String: use the most frequent item that
    is not the same as the previous item.

    Time Complexity: O(n log k)
    Space Complexity: O(k)
    """
    counts = Counter(barcodes)
    max_heap = [(-cnt, code) for code, cnt in counts.items()]
    heapq.heapify(max_heap)

    res = []
    prev = None

    while max_heap or prev:
        # Problem guarantees a solution exists, so no need for empty heap check
        cnt, code = heapq.heappop(max_heap)
        res.append(code)

        if prev:
            heapq.heappush(max_heap, prev)
            prev = None

        if cnt + 1 < 0:
            prev = (cnt + 1, code)

    return res
```

---

## 5. Course Schedule III
Maximize the number of courses taken, given durations and deadlines.

### Examples & Edge Cases
- **Example**: `courses = [[100, 200], [200, 1300], [1000, 1250], [2000, 3200]]` -> `3`
- **Edge Case: Course duration > deadline**: Impossible to take, should be ignored.

### Optimal Python Solution (Greedy + Heap)
```python
import heapq

def scheduleCourse(courses: list[list[int]]) -> int:
    """
    1. Sort courses by deadline.
    2. Try to take every course.
    3. If taking a course exceeds its deadline, remove the longest course taken so far.

    Time Complexity: O(n log n)
    Space Complexity: O(n)
    """
    # Sort by deadline to process courses in order of urgency
    courses.sort(key=lambda x: x[1])

    # Max-heap to track the durations of courses we have currently 'taken'
    taken_durations = []
    total_time = 0

    for duration, deadline in courses:
        # Optimistically take the course
        total_time += duration
        heapq.heappush(taken_durations, -duration)

        # If taking this course violates the current deadline, we must
        # drop the course with the largest duration (even if it's the current one)
        # to free up the most time for future courses.
        if total_time > deadline:
            total_time -= -heapq.heappop(taken_durations)

    return len(taken_durations)
```

### Explanation
1.  **Greedy by Deadline**: We process courses by their deadlines because finishing a course early never hurts our chances for later courses.
2.  **Greedy Replacement**: If we find ourselves past a deadline, the most efficient way to get back "on track" is to remove the course that took the longest time. This gives us the maximum "budget" for all remaining courses.

### Complexity Analysis
- **Time Complexity**: $O(n \log n)$ due to sorting. The heap operations are $O(n \log n)$ in total.
- **Space Complexity**: $O(n)$ for the heap.
