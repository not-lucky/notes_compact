# Course Schedule Problems

> **Prerequisites:** [07-topological-sort](./07-topological-sort.md)

## Interview Context

Course Schedule is a FANG+ classic because:

1. **Clean problem framing**: Dependencies as prerequisite relationships
2. **Two variations**: Can finish (cycle detection) + order (topological sort)
3. **Real-world relevance**: Build systems, package managers
4. **Tests graph fundamentals**: Graph building, cycle detection, ordering

Expect to see this problem or a variant at Meta, Google, and Amazon.

---

## Problem 1: Course Schedule I (Can Finish?)

Given `numCourses` and prerequisites where `[a, b]` means course `b` is required before course `a`, determine if you can finish all courses.

```
Example 1:
numCourses = 2
prerequisites = [[1, 0]]
Output: true
Explanation: Take 0 first, then 1.

Example 2:
numCourses = 2
prerequisites = [[1, 0], [0, 1]]
Output: false
Explanation: 0 requires 1, 1 requires 0. Cycle!
```

---

## Course Schedule I: DFS Solution

```python
from collections import defaultdict

def can_finish(numCourses: int, prerequisites: list[list[int]]) -> bool:
    """
    Check if all courses can be completed (no cycle).

    Time: O(V + E)
    Space: O(V + E)
    """
    WHITE, GRAY, BLACK = 0, 1, 2

    # Build graph: prereq -> course (b -> a for [a, b])
    graph = defaultdict(list)
    for course, prereq in prerequisites:
        graph[prereq].append(course)

    color = [WHITE] * numCourses

    def has_cycle(node: int) -> bool:
        color[node] = GRAY

        for next_course in graph[node]:
            if color[next_course] == GRAY:
                return True  # Back edge = cycle
            if color[next_course] == WHITE:
                if has_cycle(next_course):
                    return True

        color[node] = BLACK
        return False

    for course in range(numCourses):
        if color[course] == WHITE:
            if has_cycle(course):
                return False

    return True
```

---

## Course Schedule I: Kahn's Solution

```python
from collections import defaultdict, deque

def can_finish_kahn(numCourses: int, prerequisites: list[list[int]]) -> bool:
    """
    Use Kahn's algorithm: can finish if all courses are processed.

    Time: O(V + E)
    Space: O(V + E)
    """
    graph = defaultdict(list)
    in_degree = [0] * numCourses

    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1

    # Start with courses having no prerequisites
    queue = deque([c for c in range(numCourses) if in_degree[c] == 0])
    completed = 0

    while queue:
        course = queue.popleft()
        completed += 1

        for next_course in graph[course]:
            in_degree[next_course] -= 1
            if in_degree[next_course] == 0:
                queue.append(next_course)

    return completed == numCourses
```

---

## Problem 2: Course Schedule II (Find Order)

Return an ordering of courses to complete them all. If impossible, return empty array.

```
Example 1:
numCourses = 4
prerequisites = [[1,0], [2,0], [3,1], [3,2]]
Output: [0, 1, 2, 3] or [0, 2, 1, 3]

Graph:
  0 → 1 → 3
  ↓       ↑
  2 ------+
```

---

## Course Schedule II: Kahn's Solution

```python
from collections import defaultdict, deque

def find_order(numCourses: int, prerequisites: list[list[int]]) -> list[int]:
    """
    Return topological order of courses.

    Time: O(V + E)
    Space: O(V + E)
    """
    graph = defaultdict(list)
    in_degree = [0] * numCourses

    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1

    queue = deque([c for c in range(numCourses) if in_degree[c] == 0])
    order = []

    while queue:
        course = queue.popleft()
        order.append(course)

        for next_course in graph[course]:
            in_degree[next_course] -= 1
            if in_degree[next_course] == 0:
                queue.append(next_course)

    return order if len(order) == numCourses else []
```

---

## Course Schedule II: DFS Solution

```python
from collections import defaultdict

def find_order_dfs(numCourses: int, prerequisites: list[list[int]]) -> list[int]:
    """
    Return topological order using DFS (reverse post-order).

    Time: O(V + E)
    Space: O(V + E)
    """
    WHITE, GRAY, BLACK = 0, 1, 2

    graph = defaultdict(list)
    for course, prereq in prerequisites:
        graph[prereq].append(course)

    color = [WHITE] * numCourses
    order = []
    has_cycle = [False]

    def dfs(node: int):
        if has_cycle[0]:
            return

        color[node] = GRAY

        for next_course in graph[node]:
            if color[next_course] == GRAY:
                has_cycle[0] = True
                return
            if color[next_course] == WHITE:
                dfs(next_course)

        color[node] = BLACK
        order.append(node)

    for course in range(numCourses):
        if color[course] == WHITE:
            dfs(course)

    if has_cycle[0]:
        return []

    return order[::-1]  # Reverse post-order
```

---

## Common Gotchas

### 1. Edge Direction

The prerequisite `[a, b]` means `b` must come before `a`:
- Edge direction: `b → a`
- NOT `a → b` (common mistake!)

```python
# WRONG
for course, prereq in prerequisites:
    graph[course].append(prereq)  # Wrong direction!

# CORRECT
for course, prereq in prerequisites:
    graph[prereq].append(course)  # prereq -> course
```

### 2. Self-Loop

```python
prerequisites = [[1, 1]]  # Course 1 requires itself = cycle
```

### 3. Disconnected Courses

Courses with no prerequisites and no dependents are valid:

```python
numCourses = 3
prerequisites = [[1, 0]]  # Course 2 has no relations
# Valid order: [0, 2, 1] or [2, 0, 1]
```

---

## Variations

### Minimum Semesters (Parallel Courses)

```python
def minimum_semesters(n: int, relations: list[list[int]]) -> int:
    """
    Minimum semesters to complete all courses.
    Each semester, take all available courses in parallel.
    """
    graph = defaultdict(list)
    in_degree = [0] * (n + 1)  # 1-indexed

    for pre, course in relations:
        graph[pre].append(course)
        in_degree[course] += 1

    queue = deque([i for i in range(1, n + 1) if in_degree[i] == 0])
    semesters = 0
    completed = 0

    while queue:
        semesters += 1
        next_level = deque()

        for _ in range(len(queue)):
            course = queue.popleft()
            completed += 1

            for next_course in graph[course]:
                in_degree[next_course] -= 1
                if in_degree[next_course] == 0:
                    next_level.append(next_course)

        queue = next_level

    return semesters if completed == n else -1
```

### Course Schedule with K Prerequisites Limit

```python
def can_finish_with_limit(numCourses: int, prerequisites: list[list[int]],
                           k: int) -> list[int]:
    """
    Each semester, take at most k courses.
    """
    graph = defaultdict(list)
    in_degree = [0] * numCourses

    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1

    queue = deque([c for c in range(numCourses) if in_degree[c] == 0])
    order = []

    while queue:
        # Take at most k courses this semester
        semester_courses = []
        for _ in range(min(k, len(queue))):
            course = queue.popleft()
            order.append(course)
            semester_courses.append(course)

        for course in semester_courses:
            for next_course in graph[course]:
                in_degree[next_course] -= 1
                if in_degree[next_course] == 0:
                    queue.append(next_course)

    return order if len(order) == numCourses else []
```

---

## Edge Cases

```python
# 1. No prerequisites
numCourses = 3
prerequisites = []
# Any order is valid: [0, 1, 2]

# 2. Single course
numCourses = 1
prerequisites = []
# Output: [0]

# 3. Direct cycle
prerequisites = [[0, 1], [1, 0]]
# Output: [] (impossible)

# 4. Indirect cycle
prerequisites = [[1, 0], [2, 1], [0, 2]]
# Output: [] (0 → 1 → 2 → 0)

# 5. Multiple valid orders
prerequisites = [[2, 0], [2, 1]]
# Valid: [0, 1, 2] or [1, 0, 2]
```

---

## Complexity Analysis

| Operation | Time | Space |
|-----------|------|-------|
| Build graph | O(E) | O(V + E) |
| DFS/Kahn's | O(V + E) | O(V) |
| Total | O(V + E) | O(V + E) |

V = numCourses, E = len(prerequisites)

---

## Interview Tips

1. **Clarify edge direction**: `[a, b]` means `b → a`
2. **Handle empty prerequisites**: All courses can be taken in any order
3. **Know both approaches**: DFS and Kahn's
4. **Cycle = impossible**: Key insight
5. **Multiple valid orders**: Mention this if asked

---

## Practice Problems

| # | Problem | Difficulty | Key Variation |
|---|---------|------------|---------------|
| 1 | Course Schedule | Medium | Cycle detection |
| 2 | Course Schedule II | Medium | Return order |
| 3 | Parallel Courses | Medium | Minimum semesters |
| 4 | Course Schedule III | Hard | Deadline constraints |
| 5 | Course Schedule IV | Medium | Reachability queries |

---

## Key Takeaways

1. **Course Schedule I**: Just check for cycle
2. **Course Schedule II**: Return topological order
3. **Edge direction matters**: `[a, b]` means `b → a`
4. **Both algorithms work**: Kahn's often cleaner
5. **Handle disconnected**: Iterate all courses

---

## Next: [09-dijkstra.md](./09-dijkstra.md)

Learn Dijkstra's algorithm for weighted shortest paths.
