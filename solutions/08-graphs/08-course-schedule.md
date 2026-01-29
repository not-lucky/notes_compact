# Solutions: Course Schedule Problems

## Practice Problems

| #   | Problem             | Difficulty | Key Variation        |
| --- | ------------------- | ---------- | -------------------- |
| 1   | Course Schedule     | Medium     | Cycle detection      |
| 2   | Course Schedule II  | Medium     | Return order         |
| 3   | Parallel Courses    | Medium     | Minimum semesters    |
| 4   | Course Schedule III | Hard       | Deadline constraints |
| 5   | Course Schedule IV  | Medium     | Reachability queries |

---

## 1. Course Schedule

### Problem Statement

Determine if you can finish all courses given the prerequisites.

### Optimal Python Solution

```python
from collections import defaultdict

def canFinish(numCourses: int, prerequisites: list[list[int]]) -> bool:
    adj = defaultdict(list)
    for course, pre in prerequisites:
        adj[pre].append(course)

    # 0: unvisited, 1: visiting, 2: visited
    state = [0] * numCourses

    def has_cycle(u):
        if state[u] == 1: return True
        if state[u] == 2: return False

        state[u] = 1
        for v in adj[u]:
            if has_cycle(v): return True
        state[u] = 2
        return False

    for i in range(numCourses):
        if state[i] == 0:
            if has_cycle(i): return False
    return True
```

### Explanation

- **Algorithm**: DFS with 3-state coloring.
- **Cycle Detection**: If we hit a node that is currently in the recursion stack (state 1), a cycle exists.
- **Complexity**: Time O(V + E), Space O(V + E).

---

## 2. Course Schedule II

### Problem Statement

Return a valid course ordering.

### Optimal Python Solution

```python
from collections import deque, defaultdict

def findOrder(numCourses: int, prerequisites: list[list[int]]) -> list[int]:
    adj = defaultdict(list)
    in_degree = [0] * numCourses
    for course, pre in prerequisites:
        adj[pre].append(course)
        in_degree[course] += 1

    queue = deque([i for i in range(numCourses) if in_degree[i] == 0])
    order = []

    while queue:
        u = queue.popleft()
        order.append(u)
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)

    return order if len(order) == numCourses else []
```

### Explanation

- **Algorithm**: Kahn's Algorithm (BFS-based Topological Sort).
- **Complexity**: Time O(V + E), Space O(V + E).

---

## 3. Parallel Courses

### Problem Statement

Find the minimum semesters needed to finish all courses (unlimited courses per semester).

### Optimal Python Solution

```python
from collections import deque, defaultdict

def minimumSemesters(n: int, relations: list[list[int]]) -> int:
    adj = defaultdict(list)
    in_degree = [0] * (n + 1)
    for u, v in relations:
        adj[u].append(v)
        in_degree[v] += 1

    queue = deque([i for i in range(1, n + 1) if in_degree[i] == 0])
    semesters = 0
    count = 0

    while queue:
        semesters += 1
        for _ in range(len(queue)):
            u = queue.popleft()
            count += 1
            for v in adj[u]:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)

    return semesters if count == n else -1
```

### Explanation

- **Algorithm**: BFS level-order traversal on a dependency graph.
- **Complexity**: Time O(V + E), Space O(V + E).

---

## 4. Course Schedule III

### Problem Statement

Given courses with durations and deadlines, find the maximum number of courses you can take.

### Optimal Python Solution

```python
import heapq

def scheduleCourse(courses: list[list[int]]) -> int:
    # Sort courses by their deadlines
    courses.sort(key=lambda x: x[1])
    heap = [] # Max-heap for durations
    total_time = 0

    for duration, deadline in courses:
        if total_time + duration <= deadline:
            total_time += duration
            heapq.heappush(heap, -duration)
        elif heap and -heap[0] > duration:
            # Replace the longest course with the current shorter one
            total_time += duration + heapq.heappop(heap)
            heapq.heappush(heap, -duration)

    return len(heap)
```

### Explanation

- **Algorithm**: Greedy with a Max-Heap.
- **Logic**: Sort by deadlines. Always take the current course if it fits. If it doesn't fit, check if it's shorter than the longest course we've already taken. Replacing a longer course with a shorter one gives us more "buffer" for future courses.
- **Complexity**: Time O(N log N), Space O(N).

---

## 5. Course Schedule IV

### Problem Statement

Determine if course `u` is a prerequisite of course `v` for multiple queries.

### Optimal Python Solution

```python
def checkIfPrerequisite(numCourses: int, prerequisites: list[list[int]], queries: list[list[int]]) -> list[bool]:
    # Use Floyd-Warshall approach for reachability
    is_prereq = [[False] * numCourses for _ in range(numCourses)]

    for u, v in prerequisites:
        is_prereq[u][v] = True

    for k in range(numCourses):
        for i in range(numCourses):
            for j in range(numCourses):
                if is_prereq[i][k] and is_prereq[k][j]:
                    is_prereq[i][j] = True

    return [is_prereq[u][v] for u, v in queries]
```

### Explanation

- **Algorithm**: Floyd-Warshall algorithm for transitive closure.
- **Logic**: If `i` is a prereq of `k` and `k` is a prereq of `j`, then `i` is a prereq of `j`.
- **Complexity**: Time O(N³), Space O(N²). For smaller N (up to 100), this is optimal. For larger N, use multiple BFS/DFS.
