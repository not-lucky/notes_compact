import heapq

def dijkstra(n: int, edges: list[list[int]], start: int) -> dict:
    """
    Dijkstra's Shortest Path Algorithm.
    Pattern: Graph (Weighted Shortest Path)
    Time: O(E log V)
    Space: O(V + E)
    """
    adj = {i: [] for i in range(n)}
    for u, v, w in edges:
        adj[u].append((v, w))

    distances = {i: float('inf') for i in range(n)}
    distances[start] = 0
    pq = [(0, start)] # (distance, node)

    while pq:
        d, u = heapq.heappop(pq)

        if d > distances[u]:
            continue

        for v, w in adj[u]:
            if distances[u] + w < distances[v]:
                distances[v] = distances[u] + w
                heapq.heappush(pq, (distances[v], v))

    return distances

if __name__ == "__main__":
    # Test cases
    n = 4
    edges = [[0, 1, 1], [0, 2, 4], [1, 2, 2], [1, 3, 6], [2, 3, 3]]
    # 0 -> 1 (1) -> 2 (2) -> 3 (3) = 6
    # 0 -> 2 (4) -> 3 (3) = 7
    # 0 -> 1 (1) -> 3 (6) = 7
    dists = dijkstra(n, edges, 0)
    assert dists[3] == 6
    print("All tests passed!")
