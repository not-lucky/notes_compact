# Course Schedule Problems

> **Prerequisites:** [07-topological-sort](./07-topological-sort.md)

## Building Intuition

**The University Registration Mental Model**: Imagine planning your 4-year course schedule. Some courses require prerequisites:

- Data Structures requires Intro to Programming
- Algorithms requires Data Structures
- Machine Learning requires Algorithms AND Linear Algebra

**Question 1 (Can Finish?)**: Is there ANY valid order to take all courses?
**Question 2 (Find Order)**: What IS that order?

```
Prerequisites:              Dependency Graph:
ML requires Algo, LinAlg    Intro → DS → Algo → ML
Algo requires DS                         ↗
DS requires Intro           LinAlg ─────

Can we schedule? Yes! Take: Intro → DS → LinAlg → Algo → ML
```

### Step-by-Step Kahn's Algorithm Trace

Consider `numCourses = 4`, `prerequisites = [[1,0], [2,0], [3,1], [3,2]]`

1. **Calculate In-degrees**:
   - Course 0: 0
   - Course 1: 1 (from 0)
   - Course 2: 1 (from 0)
   - Course 3: 2 (from 1, 2)
2. **Initialize Queue**: Courses with in-degree 0 -> `Queue = [0]`
3. **Process 0**:
   - Pop 0. Add to order: `[0]`
   - Neighbors of 0 are 1 and 2.
   - Decrease in-degree of 1 to 0 -> add to Queue. `Queue = [1]`
   - Decrease in-degree of 2 to 0 -> add to Queue. `Queue = [1, 2]`
4. **Process 1**:
   - Pop 1. Add to order: `[0, 1]`
   - Neighbor of 1 is 3. Decrease in-degree of 3 to 1. `Queue = [2]`
5. **Process 2**:
   - Pop 2. Add to order: `[0, 1, 2]`
   - Neighbor of 2 is 3. Decrease in-degree of 3 to 0 -> add to Queue. `Queue = [3]`
6. **Process 3**:
   - Pop 3. Add to order: `[0, 1, 2, 3]`
   - No neighbors. `Queue = []`
7. **Done**. Order is `[0, 1, 2, 3]`.

### Why This Is a Graph Problem

Each course is a **node**. Each prerequisite relationship is a **directed edge**.
The input `[a, b]` means "to take course `a`, you must first complete course `b`",
which translates to a directed edge `b → a` in the graph.

Once you have this graph:
- **Course Schedule I** = "Does this graph have a cycle?" (cycle → impossible)
- **Course Schedule II** = "Give me a topological ordering of this graph"

**The cycle = impossibility insight**:
If A requires B and B requires A, neither can be taken first. This is exactly a cycle!

```
Impossible schedule:
Course A requires B        A → B
Course B requires A        B → A

This forms a cycle: A → B → A → B → ...
No valid ordering exists!
```

---

## When NOT to Use

**Course Schedule approach is overkill when:**

- No dependencies at all → Answer is trivially "yes" / "any order"
- Linear chain of dependencies → Just follow the chain
- Tree structure → Level-order traversal works

**Don't confuse with:**

- **Shortest path problems** → Different question entirely
- **Finding/returning a cycle** → We only need to detect, not return the cycle
- **Minimum spanning tree** → Wrong algorithm family

**Common mistake scenarios:**

- Wrong edge direction → `[a, b]` means `b → a`, not `a → b`
- Not handling disconnected components → Must check all courses
- Returning wrong format → II returns list of courses, not true/false

**When DFS vs BFS (Kahn's) matters:**

- Both work equally well for correctness
- Kahn's is often more intuitive (process available courses first)
- DFS is shorter code if you're comfortable with recursion
- For Course Schedule II, Kahn's builds the order naturally (no reversal needed)
- For very deep graphs (linear chains of 10^5+ nodes), Kahn's avoids stack overflow

---

## Interview Context

Course Schedule is a FANG+ classic because:

1. **Clean problem framing**: Dependencies as prerequisite relationships
2. **Two variations**: Can finish (cycle detection) + order (topological sort)
3. **Real-world relevance**: Build systems, package managers, CI pipelines
4. **Tests graph fundamentals**: Graph building, cycle detection, ordering

Expect to see this problem or a variant at Meta, Google, and Amazon.

### FANG Context: Amazon Variations
Amazon frequently tests topological sorting heavily but masks it in system design/ops scenarios:
1. **Package Dependency Resolution**: Given packages and dependencies, output the valid installation order (same as Course Schedule II).
2. **Parallel Task Execution**: What's the shortest time to finish all tasks if tasks without dependencies can be run concurrently? (See the *Minimum Semesters* variation below).
3. **Circular Dependency Detection**: Find exactly which services are forming a circular dependency in a microservices mesh.

---

## Problem 1: Course Schedule I (Can Finish?)

Given `numCourses` and prerequisites where `[a, b]` means course `b` is required before course `a`, determine if you can finish all courses.

### Theory: Directed Acyclic Graphs (DAGs)
A directed graph is a DAG if it contains no cycles. For course scheduling:
- Courses are **vertices**
- Dependencies (`[a, b]` meaning `b → a`) are directed **edges**
- If a graph has a cycle (e.g., `A → B → A`), no topological order can exist.
- Therefore, checking if we can finish all courses is exactly equivalent to **verifying the prerequisite graph is a DAG**.

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

**Approach**: Use 3-color DFS cycle detection. A back edge (hitting a GRAY node) means a cycle exists.

- WHITE (0) = unvisited
- GRAY (1) = currently being explored (on the recursion stack)
- BLACK (2) = fully processed (all descendants explored)

```python
from collections import defaultdict

def can_finish(num_courses: int, prerequisites: list[list[int]]) -> bool:
    """
    Check if all courses can be completed (no cycle in prerequisite graph).

    Time:  O(V + E) — visit each node and edge once
    Space: O(V + E) — graph storage + recursion stack
    """
    # States: 0 = unvisited, 1 = visiting (in current path), 2 = visited (fully processed)
    state = [0] * num_courses

    # Build adjacency list: prereq -> course (b -> a for [a, b])
    graph: dict[int, list[int]] = defaultdict(list)
    for course, prereq in prerequisites:
        graph[prereq].append(course)

    def has_cycle(node: int) -> bool:
        """Return True if a cycle is reachable from node."""
        if state[node] == 1:
            return True   # Back edge → cycle detected
        if state[node] == 2:
            return False  # Already fully explored

        state[node] = 1   # Mark as "in progress"

        for neighbor in graph[node]:
            if has_cycle(neighbor):
                return True

        state[node] = 2   # Mark as "fully explored"
        return False

    # Must check every connected component
    for course in range(num_courses):
        if state[course] == 0:
            if has_cycle(course):
                return False

    return True
```

---

## Course Schedule I: Kahn's (BFS) Solution

**Approach**: Repeatedly remove nodes with in-degree 0. If all nodes are removed, no cycle exists.

**Why it works**: Every DAG has at least one node with in-degree 0. Remove it, update in-degrees, repeat. If a cycle exists, the nodes in the cycle will never reach in-degree 0, so `completed < numCourses`.

```python
from collections import defaultdict, deque

def can_finish_kahn(num_courses: int, prerequisites: list[list[int]]) -> bool:
    """
    Use Kahn's algorithm: can finish iff all courses are processable.

    Time:  O(V + E) — each node enqueued/dequeued once, each edge processed once
    Space: O(V + E) — graph storage + queue
    """
    graph: dict[int, list[int]] = defaultdict(list)
    in_degree = [0] * num_courses

    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1

    # Start with courses that have no prerequisites
    queue = deque(c for c in range(num_courses) if in_degree[c] == 0)
    completed = 0

    while queue:
        course = queue.popleft()
        completed += 1

        for neighbor in graph[course]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return completed == num_courses
```

---

## Problem 2: Course Schedule II (Find Order)

Return an ordering of courses to complete them all. If impossible, return empty list.

**Key difference from Course Schedule I**: Instead of just returning `True`/`False`,
you must return the actual topological order (or `[]` if a cycle exists).

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

## Course Schedule II: Kahn's (BFS) Solution

Kahn's algorithm is the most natural fit for returning a topological order. It builds the order directly — each node is appended as it's dequeued.

**Why it works (Theory):**
Every DAG has at least one node with in-degree 0. Process it, remove its outgoing edges, and the remaining graph is still a DAG. Repeat to build a valid topological order. If the graph has a cycle, remaining nodes will have in-degree > 0 and won't be processed — so `len(order) < numCourses`.

```python
from collections import defaultdict, deque

def find_order(num_courses: int, prerequisites: list[list[int]]) -> list[int]:
    """
    Return a valid topological order, or [] if a cycle exists.

    Time:  O(V + E)
    Space: O(V + E)
    """
    graph: dict[int, list[int]] = defaultdict(list)
    in_degree = [0] * num_courses

    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1

    # Seed queue with all zero-in-degree nodes
    queue = deque(c for c in range(num_courses) if in_degree[c] == 0)
    order: list[int] = []

    while queue:
        course = queue.popleft()
        order.append(course)

        for neighbor in graph[course]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return order if len(order) == num_courses else []
```

---

## Course Schedule II: DFS Solution

**Approach**: DFS post-order gives reverse topological order. Append a node to `order` only after all its descendants are fully explored, then reverse at the end.

**Why reverse post-order works**: A node is appended only after all courses that depend on it (transitively) have been appended. Reversing this gives prerequisites-first order.

```python
from collections import defaultdict

def find_order_dfs(num_courses: int, prerequisites: list[list[int]]) -> list[int]:
    """
    Return topological order using DFS (reverse post-order).

    Time:  O(V + E)
    Space: O(V + E)
    """
    graph: dict[int, list[int]] = defaultdict(list)
    for course, prereq in prerequisites:
        graph[prereq].append(course)

    # 0 = unvisited, 1 = visiting, 2 = visited
    state = [0] * num_courses
    order: list[int] = []

    def has_cycle(node: int) -> bool:
        if state[node] == 1:
            return True
        if state[node] == 2:
            return False

        state[node] = 1

        for neighbor in graph[node]:
            if has_cycle(neighbor):
                return True

        state[node] = 2
        order.append(node)  # Post-order: append after all descendants done
        return False

    for course in range(num_courses):
        if state[course] == 0:
            if has_cycle(course):
                return []

    return order[::-1]  # Reverse post-order = topological order
```

---

## Common Gotchas

### 1. Edge Direction

The prerequisite `[a, b]` means `b` must come before `a`:

- Edge direction: `b → a`
- NOT `a → b` (most common mistake!)

```python
# WRONG — reversed edge direction
for course, prereq in prerequisites:
    graph[course].append(prereq)  # Wrong direction!

# CORRECT — prereq points to dependent course
for course, prereq in prerequisites:
    graph[prereq].append(course)  # prereq -> course
```

### 2. Self-Loop

```python
prerequisites = [[1, 1]]  # Course 1 requires itself = trivial cycle
```

Both DFS (GRAY check) and Kahn's (in-degree never reaches 0) handle this correctly.

### 3. Disconnected Courses

Courses with no prerequisites and no dependents are valid and must be included in the order:

```python
num_courses = 3
prerequisites = [[1, 0]]  # Course 2 has no relations
# Valid order: [0, 2, 1] or [2, 0, 1]
```

Both algorithms handle this: DFS iterates all nodes; Kahn's seeds all zero-in-degree nodes.

### 4. DFS Early Exit After Cycle Detection

In the DFS Course Schedule II solution, always check `has_cycle` after returning from recursive calls. Without this, you may continue exploring after a cycle is found, wasting time and potentially corrupting the order.

### 5. Returning the Cycle (Advanced)

Sometimes an interviewer asks, "If there is a cycle, return the courses involved in it." You can modify the DFS algorithm to keep track of the path.

```python
def find_cycle(num_courses: int, prerequisites: list[list[int]]) -> list[int]:
    WHITE, GRAY, BLACK = 0, 1, 2
    graph: dict[int, list[int]] = defaultdict(list)
    for course, prereq in prerequisites:
        graph[prereq].append(course)

    color = [WHITE] * num_courses
    parent = [-1] * num_courses
    cycle: list[int] = []

    def dfs(node: int) -> bool:
        color[node] = GRAY
        for neighbor in graph[node]:
            if color[neighbor] == GRAY:
                # Cycle found! Reconstruct it
                curr = node
                cycle.append(neighbor)
                while curr != neighbor:
                    cycle.append(curr)
                    curr = parent[curr]
                cycle.append(neighbor)
                cycle.reverse()
                return True
            if color[neighbor] == WHITE:
                parent[neighbor] = node
                if dfs(neighbor):
                    return True
        color[node] = BLACK
        return False

    for course in range(num_courses):
        if color[course] == WHITE:
            if dfs(course):
                return cycle
    return []
```

---

## Variations

### Minimum Semesters / Parallel Courses (LC 1136)

**Problem**: Take all available courses each semester in parallel. What's the minimum number of semesters?

**Key insight**: This is the **longest path in the DAG**, which equals the number of BFS levels in Kahn's algorithm.

> **Note**: This problem uses 1-indexed courses and `[pre, course]` format (opposite of Course Schedule's `[course, prereq]`). Always check the input format!

```python
from collections import defaultdict, deque

def minimum_semesters(n: int, relations: list[list[int]]) -> int:
    """
    Minimum semesters to complete all courses, taking all available
    courses each semester in parallel. Returns -1 if impossible (cycle).

    This is equivalent to finding the longest path in the DAG,
    computed as the number of BFS levels in Kahn's algorithm.

    Time:  O(V + E)
    Space: O(V + E)
    """
    graph: dict[int, list[int]] = defaultdict(list)
    in_degree = [0] * (n + 1)  # 1-indexed courses

    for prereq, course in relations:  # Note: [pre, course] format
        graph[prereq].append(course)
        in_degree[course] += 1

    queue = deque(i for i in range(1, n + 1) if in_degree[i] == 0)

    semesters = 0
    completed = 0

    while queue:
        semesters += 1
        # Process all courses available this semester
        for _ in range(len(queue)):
            course = queue.popleft()
            completed += 1

            for neighbor in graph[course]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

    return semesters if completed == n else -1
```

### Course Schedule with Per-Semester Limit

**Problem**: You can take at most `k` courses per semester. Return a valid semester-by-semester schedule. (Note: Finding the *minimum* number of semesters with a limit `k` is NP-Hard, like LC 1494 Parallel Courses II. This greedy approach just finds *a* valid schedule).

```python
from collections import defaultdict, deque

def schedule_with_limit(
    num_courses: int, prerequisites: list[list[int]], k: int
) -> list[list[int]]:
    """
    Return a valid schedule taking at most k courses per semester.
    Returns [] if impossible (cycle).

    Time:  O(V + E)
    Space: O(V + E)
    """
    graph: dict[int, list[int]] = defaultdict(list)
    in_degree = [0] * num_courses

    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1

    # Using a list and sorting to prioritize courses (e.g., those unlocking more courses)
    # is often needed in real variations, but here we just use a simple queue.
    queue = deque(c for c in range(num_courses) if in_degree[c] == 0)
    schedule: list[list[int]] = []
    completed = 0

    while queue:
        # Take at most k courses this semester from available ones
        semester_size = min(k, len(queue))
        semester_courses: list[int] = []

        for _ in range(semester_size):
            course = queue.popleft()
            semester_courses.append(course)
            completed += 1
            
        schedule.append(semester_courses)

        # Unlock dependent courses only after the semester is over
        # This is crucial: courses taken this semester only unlock their dependents
        # for the NEXT semester.
        for course in semester_courses:
            for neighbor in graph[course]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

    return schedule if completed == num_courses else []
```

---

## Edge Cases

```python
# 1. No prerequisites — any order is valid
num_courses = 3
prerequisites = []
# Output: [0, 1, 2] (or any permutation)

# 2. Single course
num_courses = 1
prerequisites = []
# Output: [0]

# 3. Direct cycle
prerequisites = [[0, 1], [1, 0]]
# Output: [] (impossible)

# 4. Indirect cycle
prerequisites = [[1, 0], [2, 1], [0, 2]]
# Output: [] (0 → 1 → 2 → 0)

# 5. Multiple valid orders (topological order is not unique)
prerequisites = [[2, 0], [2, 1]]
# Valid: [0, 1, 2] or [1, 0, 2]
```

---

## Complexity Analysis

| Operation   | Time     | Space    |
| ----------- | -------- | -------- |
| Build graph | O(E)     | O(V + E) |
| DFS/Kahn's  | O(V + E) | O(V)     |
| **Total**   | **O(V + E)** | **O(V + E)** |

Where V = `numCourses`, E = `len(prerequisites)`.

**Space breakdown**:
- Graph adjacency list: O(V + E)
- Color array / in-degree array: O(V)
- Queue (Kahn's) or recursion stack (DFS): O(V) worst case
- Output order (Course Schedule II): O(V)

### Complexity Trade-offs: Kahn's (BFS) vs DFS

| Aspect               | Kahn's Algorithm (BFS)                                             | Recursive DFS                                                      |
|-----------------------|--------------------------------------------------------------------|--------------------------------------------------------------------|
| **Space**             | Explicit queue, O(V)                                               | Implicit call stack, O(V) worst case                               |
| **Stack Overflow**    | Safe — uses explicit data structures                               | Risky — a linear chain of 10^5 courses can hit Python's recursion limit |
| **Ordering**          | Naturally builds topological order. Easy to extend to lexicographic order using a min-heap (O(V log V)) | Produces reverse post-order; must reverse at end. Harder to enforce secondary ordering |
| **Parallel Tasks**    | Counts "semesters" naturally by processing level by level           | Requires passing/tracking depth through recursion                  |
| **Cycle Reporting**   | Detects cycle if `completed < V`. Hard to identify *which* nodes form the cycle | Easier to trace the exact cycle path via the GRAY nodes on the stack |

**Recommendation**: Prefer Kahn's for Course Schedule problems. It avoids recursion depth issues, builds the order naturally, and extends to parallel/semester variations out of the box.

---

## Interview Tips

1. **Clarify edge direction first**: `[a, b]` means `b → a` — state this explicitly to the interviewer
2. **Handle empty prerequisites**: All courses can be taken in any order
3. **Know both approaches**: DFS and Kahn's — interviewer may ask you to implement both
4. **Cycle = impossible**: The core insight; state it upfront
5. **Multiple valid orders**: Mention that topological order is not unique
6. **Default to Kahn's**: Unless the interviewer asks for DFS — it's safer and more extensible

---

## Practice Problems

| #   | Problem                                                                                  | Difficulty | Key Concept                                    | Hint                                                                 |
| --- | ---------------------------------------------------------------------------------------- | ---------- | ---------------------------------------------- | -------------------------------------------------------------------- |
| 1   | [207. Course Schedule](https://leetcode.com/problems/course-schedule/)                   | Medium     | Cycle detection in directed graph              | Kahn's: do all nodes reach in-degree 0? DFS: any back edges?         |
| 2   | [210. Course Schedule II](https://leetcode.com/problems/course-schedule-ii/)             | Medium     | Return topological order                       | Same as #1 but collect the order. Kahn's: append on dequeue. DFS: reverse post-order |
| 3   | [1136. Parallel Courses](https://leetcode.com/problems/parallel-courses/)                | Medium     | Longest path in DAG / BFS levels               | Level-order Kahn's — answer is the number of BFS levels              |
| 4   | [2115. Find All Possible Recipes from Given Supplies](https://leetcode.com/problems/find-all-possible-recipes-from-given-supplies/) | Medium     | Topological sort with external dependencies    | Model supplies as nodes with in-degree 0; run Kahn's on recipes      |
| 5   | [1462. Course Schedule IV](https://leetcode.com/problems/course-schedule-iv/)            | Medium     | Reachability / transitive closure              | BFS/DFS from each node, or Floyd-Warshall for all-pairs reachability |

**Note on Course Schedule III (LC 630)**: Despite the name, it is a **greedy/heap** problem about deadlines, not a graph/topological sort problem. Don't confuse it with this family.

---

## Key Takeaways

1. **Course Schedule I** = cycle detection → "Is this a DAG?"
2. **Course Schedule II** = topological sort → "Give me a valid ordering"
3. **Edge direction matters**: `[a, b]` means `b → a` (the #1 mistake)
4. **Two algorithms**: Kahn's (BFS, preferred) and DFS (3-color)
5. **Handle disconnected components**: Iterate all courses, not just those in prerequisites
6. **Cycle ↔ impossibility**: No topological order exists iff the graph has a cycle

---

## Next: [09-dijkstra.md](./09-dijkstra.md)

Learn Dijkstra's algorithm for weighted shortest paths.
