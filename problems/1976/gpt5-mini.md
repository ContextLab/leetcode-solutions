# [Problem 1976: Number of Ways to Arrive at Destination](https://leetcode.com/problems/number-of-ways-to-arrive-at-destination/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
This asks for the number of ways to go from node 0 to node n-1 with the shortest possible travel time. When I see "shortest" with weighted edges I think Dijkstra. We need not just the shortest distance but also count how many distinct paths achieve that shortest distance. A standard modification of Dijkstra keeps a ways[] array: ways[u] = number of shortest paths from source to u. When relaxing an edge, if we find a strictly shorter distance to v we set ways[v] = ways[u]; if we find an equal shortest distance we add ways[u] to ways[v]. Remember to mod the result. Graph is undirected so add edges both ways.

Edge cases: very large edge weights (use Python ints), possibly n=1 (start==destination), and ensure modulo arithmetic. Complexity should be O(E log V) with heap.

## Refining the problem, round 2 thoughts
- Build adjacency list for undirected roads.
- Use a min-heap (priority queue) for Dijkstra. Initialize dist[0]=0 and ways[0]=1.
- While popping (d,u): if d > dist[u] skip. For each neighbor v with weight w:
  - nd = d + w
  - if nd < dist[v]: update dist[v] and ways[v] = ways[u]; push (nd, v)
  - elif nd == dist[v]: ways[v] = (ways[v] + ways[u]) % MOD
- We can return ways[n-1] modulo 1e9+7 at the end. Optionally, we can early-return when we pop node n-1 because by the time it is popped, all nodes with distance < dist[n-1] have been processed and thus all contributions to ways[n-1] from their relaxations have been applied.
- Complexity: O((V + E) log V) ~ O(E log V) which is fine for n <= 200 and up to ~20k edges.

## Attempted solution(s)
```python
import heapq

class Solution:
    def countPaths(self, n: int, roads: list[list[int]]) -> int:
        MOD = 10**9 + 7
        # Build adjacency list
        adj = [[] for _ in range(n)]
        for u, v, t in roads:
            adj[u].append((v, t))
            adj[v].append((u, t))
        
        dist = [float('inf')] * n
        ways = [0] * n
        
        dist[0] = 0
        ways[0] = 1
        heap = [(0, 0)]  # (distance, node)
        
        while heap:
            d, u = heapq.heappop(heap)
            if d > dist[u]:
                continue
            # Optional early exit: by this time all contributions to ways[u] are accounted for
            if u == n - 1:
                return ways[u] % MOD
            for v, w in adj[u]:
                nd = d + w
                if nd < dist[v]:
                    dist[v] = nd
                    ways[v] = ways[u]
                    heapq.heappush(heap, (nd, v))
                elif nd == dist[v]:
                    ways[v] = (ways[v] + ways[u]) % MOD
        
        return ways[n - 1] % MOD
```
- Notes:
  - This is Dijkstra with path counting. When a strictly shorter distance to a node is found, the count is replaced; when an equal distance is found, counts are accumulated.
  - We use a min-heap for extracting the current smallest distance node. Skipping outdated heap entries (d > dist[u]) is necessary.
  - Early return when popping the destination is safe because any other node that could contribute to destination's shortest paths must have distance strictly less than dest's distance and would have been processed already.
  - Time complexity: O(E log V) where V = n and E = len(roads). Space complexity: O(V + E) for adjacency and auxiliary arrays.