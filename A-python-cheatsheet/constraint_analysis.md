# Constraint Analysis: From $N$ to Complexity

In a coding interview, the input size $N$ is your strongest hint for the expected time complexity. Most online judges (LeetCode, Codeforces) and interview environments have a **~1-second execution limit**, which roughly corresponds to **$10^7$ to $10^8$ operations**.

## The Golden Rule of $10^8$
Python is generally slower than C++, so aim for **$10^7$ operations** to be safe in a 1-second window.

| Input Size ($N$) | Expected Complexity | Possible Algorithms |
| :--- | :--- | :--- |
| $N \le 10$ | $O(N!)$ or $O(N^2 \cdot N!)$ | Permutations, Traveling Salesman (Brute Force) |
| $N \le 20$ | $O(2^N)$ | Subsets, Bitmask DP, Meet-in-the-middle |
| $N \le 100$ | $O(N^4)$ | Fourth-degree polynomial DP |
| $N \le 500$ | $O(N^3)$ | Floyd-Warshall, Matrix Multiplication, $O(N^3)$ DP |
| $N \le 5,000$ | $O(N^2)$ | Nested loops, Bubble/Insertion Sort, $O(N^2)$ DP |
| $N \le 2 \cdot 10^5$ | $O(N \log N)$ | Merge Sort, Heap Sort, Binary Search + Greedy, Segment Trees |
| $N \le 10^6$ | $O(N)$ | Linear scan, Sliding Window, Two Pointers, Hash Maps |
| $N > 10^6$ | $O(\log N)$ or $O(1)$ | Binary Search on answer, Mathematical formulas, GCD |

---

## Big-O Limit Guidelines (1-Second Window)

| Complexity | Max $N$ for 1s (Approx) |
| :--- | :--- |
| $O(1)$ | No limit |
| $O(\log N)$ | No limit |
| $O(N)$ | $10^7$ |
| $O(N \log N)$ | $10^6$ |
| $O(N^2)$ | $5,000$ |
| $O(N^3)$ | $500$ |
| $O(2^N)$ | $20 - 25$ |
| $O(N!)$ | $10 - 11$ |

### Why these limits?
- **$O(N^2)$ at $N=10,000$**: $10,000^2 = 10^8$. In Python, this will almost certainly Time Limit Exceeded (TLE).
- **$O(N \log N)$ at $N=10^6$**: $10^6 \cdot 20 \approx 2 \cdot 10^7$. This is usually the upper bound for $N \log N$ in Python.

---

## Meta-Cognitive Strategy: The "Constraint Trap"

1.  **Read constraints first**: Before thinking of an algorithm, look at $N$.
2.  **Work backwards**: If $N=10^5$, don't even consider $O(N^2)$. You *must* find an $O(N \log N)$ or $O(N)$ solution.
3.  **The "Hidden" $N$**: Sometimes the constraint is on the sum of $N$ across test cases, or on multiple variables (e.g., $N$ nodes and $M$ edges).
4.  **Space Matters**: If $N=10^6$, an $O(N)$ space complexity is fine (~4-8MB for integers), but $O(N^2)$ space will Memory Limit Exceeded (MLE).

---

## Real-World Scaling vs. Interviews

| Scenario | Optimization Focus |
| :--- | :--- |
| **Interviews** | Asymptotic complexity ($O(N)$ vs $O(N^2)$) |
| **System Design** | Latency, Throughput, IOPS, Network overhead |
| **High Frequency Trading** | Constant factors, Cache locality, L1/L2 hits |
| **Big Data (Spark)** | Data shuffling, Network I/O, Serialization |
