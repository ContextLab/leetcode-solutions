# [Problem 1334: Find the City With the Smallest Number of Neighbors at a Threshold Distance](https://leetcode.com/problems/find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need the number of reachable cities within distanceThreshold for every city, then pick the city with the smallest count (break ties by choosing the largest index). That sounds like an all-pairs shortest-paths problem so I can know the shortest distance between every pair. Given n ≤ 100, Floyd–Warshall (O(n^3)) is simple and fine. Alternatively I could run Dijkstra from each node (O(n * (m log n))) which is fine too, but Floyd–Warshall is simpler to implement and less error-prone here. Must be careful to treat the graph as undirected and set distance to 0 for same-node. Also tie-breaking: if counts equal, return the city with the greater index.

## Refining the problem, round 2 thoughts
- Edge cases: disconnected nodes will have infinite distance — they should not be counted.
- Multiple edges between same pair: constraints say all pairs are distinct, but I'll still take min(weight, existing) for safety.
- Implementation detail: initialize distances with a large INF, set self-distances to 0, set both directions for edges, run the triple loop for Floyd–Warshall.
- Counting: for each city i count j != i with dist[i][j] <= threshold.
- Tie-breaking: if multiple cities have same smallest count, return the maximum index — so when iterating in increasing index, use <= when updating the best candidate so later (larger) index replaces earlier one when counts tie.
- Complexity: Floyd–Warshall O(n^3) = at most 1e6 iterations (n<=100) which is fine. Space O(n^2).

## Attempted solution(s)
```python
class Solution:
    def findTheCity(self, n: int, edges: list[list[int]], distanceThreshold: int) -> int:
        INF = 10**9
        # Initialize distance matrix
        dist = [[INF] * n for _ in range(n)]
        for i in range(n):
            dist[i][i] = 0

        # Fill direct edges (undirected)
        for u, v, w in edges:
            if w < dist[u][v]:
                dist[u][v] = w
                dist[v][u] = w

        # Floyd-Warshall for all-pairs shortest paths
        for k in range(n):
            for i in range(n):
                # small micro-optimization: skip if dist[i][k] is INF
                if dist[i][k] == INF:
                    continue
                for j in range(n):
                    if dist[k][j] == INF:
                        continue
                    nd = dist[i][k] + dist[k][j]
                    if nd < dist[i][j]:
                        dist[i][j] = nd

        # Count reachable cities within threshold for each city
        best_city = -1
        best_count = INF  # we want minimum count
        for i in range(n):
            cnt = 0
            for j in range(n):
                if i != j and dist[i][j] <= distanceThreshold:
                    cnt += 1
            # update: choose smaller count, tie -> larger index
            if cnt <= best_count:
                best_count = cnt
                best_city = i

        return best_city
```
- Notes:
  - Approach: Floyd–Warshall computes shortest distances between all pairs. Then for each city count how many other cities are within distanceThreshold. Keep track of the minimum count and, on ties, prefer the larger index by updating when count is <= current best.
  - Time complexity: O(n^3) for Floyd–Warshall (n ≤ 100, so <= 1e6 inner iterations approximately when accounting loops) plus O(n^2) for counting — overall O(n^3).
  - Space complexity: O(n^2) to store the distance matrix.
  - Alternative: run Dijkstra from every node (O(n * (m log n))) which can be preferable for sparse graphs, but Floyd–Warshall is straightforward and sufficiently efficient here.