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

### 3. Course Schedule
**Difficulty:** Medium
**Concept:** Cycle detection

```python
from collections import defaultdict, deque
from typing import List

def can_finish(num_courses: int, prerequisites: List[List[int]]) -> bool:
    """
    Check if all courses can be finished.

    Time: O(V + E)
    Space: O(V + E)
    """
    graph = defaultdict(list)
    in_degree = [0] * num_courses
    for a, b in prerequisites:
        graph[b].append(a)
        in_degree[a] += 1

    queue = deque([i for i in range(num_courses) if in_degree[i] == 0])
    count = 0
    while queue:
        node = queue.popleft()
        count += 1
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return count == num_courses
```

### 4. Alien Dictionary
**Difficulty:** Hard
**Concept:** Build graph from constraints

```python
from collections import defaultdict, deque
from typing import List

def alien_order(words: List[str]) -> str:
    """
    Derive alien alphabet order from sorted words.

    Time: O(C)
    Space: O(1)
    """
    graph = defaultdict(set)
    in_degree = {c: 0 for word in words for c in word}

    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i+1]
        if len(w1) > len(w2) and w1.startswith(w2):
            return ""

        for c1, c2 in zip(w1, w2):
            if c1 != c2:
                if c2 not in graph[c1]:
                    graph[c1].add(c2)
                    in_degree[c2] += 1
                break

    queue = deque([c for c in in_degree if in_degree[c] == 0])
    result = []
    while queue:
        c = queue.popleft()
        result.append(c)
        for neighbor in graph[c]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return "".join(result) if len(result) == len(in_degree) else ""
```

### 5. Sequence Reconstruction
**Difficulty:** Medium
**Concept:** Unique order check

```python
from collections import defaultdict, deque
from typing import List

def sequence_reconstruction(nums: List[int], sequences: List[List[int]]) -> bool:
    """
    Check if nums is the unique shortest supersequence.

    Time: O(V + E)
    Space: O(V + E)
    """
    graph = defaultdict(list)
    in_degree = {num: 0 for num in nums}
    nodes = set()

    for seq in sequences:
        for x in seq:
            nodes.add(x)
        for i in range(len(seq) - 1):
            u, v = seq[i], seq[i+1]
            graph[u].append(v)
            if v in in_degree:
                in_degree[v] += 1
            else:
                return False

    if nodes != set(nums):
        return False

    queue = deque([n for n in in_degree if in_degree[n] == 0])
    result = []
    while queue:
        if len(queue) > 1: return False # Not unique
        u = queue.popleft()
        result.append(u)
        for v in graph[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)

    return result == nums
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
