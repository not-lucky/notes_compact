# Solutions: Topological Sort

## Practice Problems

| # | Problem | Difficulty | Key Variation |
|---|---------|------------|---------------|
| 1 | Course Schedule | Medium | Cycle detection |
| 2 | Course Schedule II | Medium | Return order |
| 3 | Alien Dictionary | Hard | Build graph from constraints |
| 4 | Parallel Courses | Medium | Minimum levels |
| 5 | Sequence Reconstruction | Medium | Unique order check |

---

## 1. Course Schedule

### Problem Statement
Check if all courses can be finished.

### Optimal Python Solution

```python
from collections import deque, defaultdict

def canFinish(numCourses: int, prerequisites: list[list[int]]) -> bool:
    adj = defaultdict(list)
    in_degree = [0] * numCourses
    for course, pre in prerequisites:
        adj[pre].append(course)
        in_degree[course] += 1

    queue = deque([i for i in range(numCourses) if in_degree[i] == 0])
    count = 0

    while queue:
        node = queue.popleft()
        count += 1
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return count == numCourses
```

### Explanation
- **Algorithm**: Kahn's Algorithm (BFS).
- **Logic**: If we can't process all nodes, there must be a cycle.
- **Complexity**: Time O(V + E), Space O(V + E).

---

## 2. Course Schedule II

### Problem Statement
Return the ordering of courses.

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
        node = queue.popleft()
        order.append(node)
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return order if len(order) == numCourses else []
```

### Explanation
- **Algorithm**: Kahn's Algorithm. The nodes are appended to the result in topological order.
- **Complexity**: Time O(V + E), Space O(V + E).

---

## 3. Alien Dictionary

### Problem Statement
Given a list of words from an alien language sorted lexicographically, find the order of characters in this language.

### Optimal Python Solution

```python
from collections import deque, defaultdict

def alienOrder(words: list[str]) -> str:
    adj = defaultdict(set)
    in_degree = {char: 0 for word in words for char in word}

    # Build graph
    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i+1]
        min_len = min(len(w1), len(w2))
        # Edge case: prefix check
        if len(w1) > len(w2) and w1[:min_len] == w2[:min_len]:
            return ""

        for j in range(min_len):
            if w1[j] != w2[j]:
                if w2[j] not in adj[w1[j]]:
                    adj[w1[j]].add(w2[j])
                    in_degree[w2[j]] += 1
                break

    # Kahn's Algorithm
    queue = deque([char for char in in_degree if in_degree[char] == 0])
    res = []

    while queue:
        char = queue.popleft()
        res.append(char)
        for neighbor in adj[char]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(res) < len(in_degree):
        return ""
    return "".join(res)
```

### Explanation
- **Concept**: Compare adjacent words to find character priorities.
- **Algorithm**: Build an adjacency list and use Kahn's algorithm for topological sort.
- **Complexity**: Time O(C) where C is the total number of characters in all words. Space O(1) or O(min(U, N)) where U is unique characters.

---

## 4. Parallel Courses

### Problem Statement
Find the minimum semesters needed to finish all courses if you can take as many as you want in parallel.

### Optimal Python Solution

```python
from collections import deque, defaultdict

def minimumSemesters(n: int, relations: list[list[int]]) -> int:
    adj = defaultdict(list)
    in_degree = [0] * (n + 1)
    for pre, course in relations:
        adj[pre].append(course)
        in_degree[course] += 1

    queue = deque([i for i in range(1, n + 1) if in_degree[i] == 0])
    semesters = 0
    courses_taken = 0

    while queue:
        semesters += 1
        for _ in range(len(queue)):
            curr = queue.popleft()
            courses_taken += 1
            for neighbor in adj[curr]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

    return semesters if courses_taken == n else -1
```

### Explanation
- **Concept**: Each "level" in Kahn's algorithm represents a semester.
- **Algorithm**: BFS with level tracking.
- **Complexity**: Time O(V + E), Space O(V + E).

---

## 5. Sequence Reconstruction

### Problem Statement
Check if a sequence `nums` can be uniquely reconstructed from a set of `sequences`.

### Optimal Python Solution

```python
from collections import deque, defaultdict

def sequenceReconstruction(nums: list[int], sequences: list[list[int]]) -> bool:
    adj = defaultdict(list)
    in_degree = {num: 0 for num in nums}
    nodes = set()

    for seq in sequences:
        for i in range(len(seq)):
            nodes.add(seq[i])
            if i > 0:
                adj[seq[i-1]].append(seq[i])
                in_degree[seq[i]] += 1

    if nodes != set(nums): return False

    queue = deque([i for i in in_degree if in_degree[i] == 0])
    res = []

    while queue:
        if len(queue) > 1: return False # More than one option means not unique
        curr = queue.popleft()
        res.append(curr)
        for neighbor in adj[curr]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return res == nums
```

### Explanation
- **Unique Order**: A topological sort is unique if and only if at every step of Kahn's algorithm, the queue has exactly one node.
- **Complexity**: Time O(V + E), Space O(V + E).
