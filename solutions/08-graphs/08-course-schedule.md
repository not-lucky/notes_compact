# Course Schedule Problems

## Practice Problems

### 1. Course Schedule
**Difficulty:** Medium
**Concept:** Cycle detection

```python
from collections import defaultdict
from typing import List

def can_finish(num_courses: int, prerequisites: List[List[int]]) -> bool:
    """
    Check if all courses can be completed (no cycle).

    >>> can_finish(2, [[1,0]])
    True
    >>> can_finish(2, [[1,0],[0,1]])
    False

    Time: O(V + E)
    Space: O(V + E)
    """
    graph = defaultdict(list)
    for course, prereq in prerequisites:
        graph[prereq].append(course)

    visited = [0] * num_courses # 0: WHITE, 1: GRAY, 2: BLACK

    def has_cycle(node: int) -> bool:
        visited[node] = 1 # GRAY
        for neighbor in graph[node]:
            if visited[neighbor] == 1:
                return True
            if visited[neighbor] == 0:
                if has_cycle(neighbor):
                    return True
        visited[node] = 2 # BLACK
        return False

    for i in range(num_courses):
        if visited[i] == 0:
            if has_cycle(i):
                return False
    return True
```

### 2. Course Schedule II
**Difficulty:** Medium
**Concept:** Return order

```python
from collections import defaultdict, deque
from typing import List

def find_order(num_courses: int, prerequisites: List[List[int]]) -> List[int]:
    """
    Return topological order of courses.

    >>> find_order(2, [[1,0]])
    [0, 1]
    >>> find_order(4, [[1,0],[2,0],[3,1],[3,2]])
    [0, 1, 2, 3]

    Time: O(V + E)
    Space: O(V + E)
    """
    graph = defaultdict(list)
    in_degree = [0] * num_courses
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1

    queue = deque([i for i in range(num_courses) if in_degree[i] == 0])
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return order if len(order) == num_courses else []
```

### 3. Parallel Courses
**Difficulty:** Medium
**Concept:** Minimum semesters

```python
from collections import defaultdict, deque
from typing import List

def minimum_semesters(n: int, relations: List[List[int]]) -> int:
    """
    Minimum semesters to complete all courses.

    >>> minimum_semesters(3, [[1,3],[2,3]])
    2
    >>> minimum_semesters(3, [[1,2],[2,3],[3,1]])
    -1

    Time: O(V + E)
    Space: O(V + E)
    """
    graph = defaultdict(list)
    in_degree = [0] * (n + 1)
    for u, v in relations:
        graph[u].append(v)
        in_degree[v] += 1

    queue = deque([i for i in range(1, n + 1) if in_degree[i] == 0])
    semesters = 0
    completed = 0

    while queue:
        semesters += 1
        for _ in range(len(queue)):
            course = queue.popleft()
            completed += 1
            for next_course in graph[course]:
                in_degree[next_course] -= 1
                if in_degree[next_course] == 0:
                    queue.append(next_course)

    return semesters if completed == n else -1
```

### 4. Course Schedule IV
**Difficulty:** Medium
**Concept:** Reachability queries

```python
from typing import List

def check_if_prerequisite(num_courses: int, prerequisites: List[List[int]],
                          queries: List[List[int]]) -> List[bool]:
    """
    There are a total of numCourses courses you have to take.
    Some courses may have prerequisites.
    Given queries[i] = [u, v], return true if u is a prerequisite of v.

    Time: O(V^3) for Floyd-Warshall or O(Q + V*(V+E)) for BFS from each node
    Space: O(V^2)
    """
    # Floyd-Warshall for transitive closure (reachability)
    reachable = [[False] * num_courses for _ in range(num_courses)]
    for u, v in prerequisites:
        reachable[u][v] = True

    for k in range(num_courses):
        for i in range(num_courses):
            for j in range(num_courses):
                if reachable[i][k] and reachable[k][j]:
                    reachable[i][j] = True

    return [reachable[u][v] for u, v in queries]
```
