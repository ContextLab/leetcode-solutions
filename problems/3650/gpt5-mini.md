# [Problem 3650: Minimum Cost Path with Edge Reversals](https://leetcode.com/problems/minimum-cost-path-with-edge-reversals/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We have a directed weighted graph. Each node has a one-time switch allowing, upon arrival, to reverse one of its incoming edges and immediately traverse it at cost 2*w. We want the minimum cost from 0 to n-1.

At first glance this looks like we must track which node switches have been used (a large state space). But think about what a single reversal does in a path: if there is an original edge u -> v with weight w, using v's switch allows moving v -> u at cost 2*w. So from a path perspective we can traverse u->v at cost w or traverse v->u at cost 2*w (but using v's switch). The "at most once" constraint is per node per path. Because all weights are positive, any shortest path will be simple (won't revisit nodes), so in any optimal path each node appears at most once and thus you cannot use the same node's switch twice on an optimal path. That suggests we can model every possible reversed move v->u with weight 2*w as a legitimate edge in the graph and then run standard Dijkstra.

So simple idea: for each original edge (u, v, w) add (u->v, w) and also (v->u, 2*w). Then run Dijkstra from 0 to n-1. This implicitly allows using a node's switch at most once per path because shortest paths are simple with positive weights.

## Refining the problem, round 2 thoughts
- Confirm correctness: adding reversed edges doesn't enforce "use at most once" explicitly, but since weights > 0, an optimal path will not revisit a node (would create a positive-cost cycle), so a node's reversed edges will be used at most once in any shortest path.
- Edge cases: unreachable destination -> return -1.
- Complexity constraints: n up to 5e4, edges up to 1e5 so building 2*m adjacency edges is fine. Dijkstra with heap is O((n + m) log n) which is acceptable.
- Memory: adjacency list with 2*m entries is fine.
- Implementation details: use heapq, distances initialized to inf, standard Dijkstra early-exit when we pop target.

## Attempted solution(s)
```python
import heapq
from typing import List

class Solution:
    def minimumCost(self, n: int, edges: List[List[int]]) -> int:
        # Build adjacency list. For each edge u->v with weight w:
        # - add forward edge u->v weight w
        # - add "reversed via switch" edge v->u weight 2*w
        graph = [[] for _ in range(n)]
        for u, v, w in edges:
            graph[u].append((v, w))
            graph[v].append((u, 2 * w))
        
        # Dijkstra from 0 to n-1
        INF = 10**18
        dist = [INF] * n
        dist[0] = 0
        heap = [(0, 0)]  # (distance, node)
        
        while heap:
            d, node = heapq.heappop(heap)
            if d != dist[node]:
                continue
            if node == n - 1:
                return d
            for nei, w in graph[node]:
                nd = d + w
                if nd < dist[nei]:
                    dist[nei] = nd
                    heapq.heappush(heap, (nd, nei))
        return -1 if dist[n-1] == INF else dist[n-1]
```
- Notes on the solution:
  - Approach: Transform each original directed edge u->v (w) into two directed edges: u->v (w) and v->u (2*w). Then compute shortest path with Dijkstra.
  - Correctness justification: Adding reversed edges captures the allowed "reverse-and-immediately-traverse" operation from a node. Since edge weights are positive, any shortest path is simple (no repeated nodes), so no shortest path will reuse a single node's switch more than once. Thus the transformed graph correctly models the problem.
  - Time complexity: Building adjacency O(m). Dijkstra runs in O((n + m) log n) (here m is original edge count, adjacency has ~2m edges).
  - Space complexity: O(n + m) for adjacency and distance arrays.