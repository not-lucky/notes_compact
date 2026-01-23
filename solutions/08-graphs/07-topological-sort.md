# Topological Sort

## Practice Problems

### 1. Course Schedule II
**Difficulty:** Medium
**Concept:** Return order

```python
from collections import defaultdict, deque
from typing import List

def find_order(num_courses: int, prerequisites: List[List[int]]) -> List[int]:
    """
    There are a total of num_courses courses you have to take, labeled from 0 to num_courses - 1.
    You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates
    that you must take course bi first if you want to take course ai.
    Return the ordering of courses you should take to finish all courses.
    If there are many valid answers, return any of them. If it is impossible
    to finish all courses, return an empty array.

    >>> find_order(2, [[1,0]])
    [0, 1]
    >>> find_order(4, [[1,0],[2,0],[3,1],[3,2]])
    [0, 1, 2, 3]

    Time: O(V + E)
    Space: O(V + E)
    """
    graph = defaultdict(list)
    in_degree = [0] * num_courses

    for a, b in prerequisites:
        graph[b].append(a)
        in_degree[a] += 1

    queue = deque([i for i in range(num_courses) if in_degree[i] == 0])
    result = []

    while queue:
        node = queue.popleft()
        result.append(node)

        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return result if len(result) == num_courses else []
```

### 2. Parallel Courses
**Difficulty:** Medium
**Concept:** Minimum levels

```python
from collections import defaultdict, deque
from typing import List

def minimum_semesters(n: int, relations: List[List[int]]) -> int:
    """
    You are given an integer n, which represents the number of courses.
    You are also given an array relations where relations[i] = [prevCoursei, nextCoursei],
    representing a prerequisite relationship.
    In one semester, you can take any number of courses as long as you have
    taken all the prerequisites in the previous semesters for the courses you are taking.
    Return the minimum number of semesters needed to take all courses.
    If there is no way to take all the courses, return -1.

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
    taken = 0

    while queue:
        semesters += 1
        for _ in range(len(queue)):
            node = queue.popleft()
            taken += 1
            for neighbor in graph[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

    return semesters if taken == n else -1
```
